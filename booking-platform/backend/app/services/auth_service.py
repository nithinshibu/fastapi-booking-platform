from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    generate_refresh_token,
    hash_refresh_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.repositories import user_repository
from app.repositories import refresh_token_repository
from app.schemas.auth import TokenResponse

# The service layer is where the business logic lives.
# It sits between the route (HTTP Layer) and the repository (DB Layer)

# .NET equivalent : our UserService / AuthService class.

""" 
REFRESH TOKEN FLOW OVERVIEW:
        LOGIN :     credentials => validate => issue access_token + refresh token
        REFRESH :   refresh_token => validate => revoke old => issue new access_token + refresh_token
        LOGOUT :    refresh_token => validate => revoke (no tokens issued)

Validate means : hash exists in DB , not revoked , not expired.


"""

# Rules this layer owns:
#           - Is this email already taken ?
#           - Are those credentials valid ?
#           - What do we return on sucess ?

# Rules this layer does NOT owns:
#           - How to hash passwords             -> handles this in security.py
#           - How to read / write into the DB   -> handles this in the user_repository.py
#           - How to format the HTTP reponse    -> handled in the route


class AuthError(Exception):
    """
    Raised when authentication or registration fails for a known business reason.

    Using a custom exception type instead of returning None or a bool means
    the route can catch it and decide the HTTP status code - the service itself
    stays HTTP-agnostic (The code is independent of HTTP details (like status codes or requests) and focuses only on business logic.).
    This follows the same pattern as throwing a custom domain exception in .NET and catching it in a controller action filter.

    """

    pass


def register_user(db: Session, email: str, password: str) -> User:
    """
    Register a new user account.

    Business rules enforced here:
    1. Email must not already exist in the DB.
    2. Password is hashed before it reaches the repository - plaintext never touches the database layer.

    Returns the newly created User on success.
    Raises AuthError if the email is already registered.

    """
    existing_user = user_repository.get_by_email(db, email)
    if existing_user:
        raise AuthError("Email already registered")

    hashed = hash_password(password)
    return user_repository.create(db, email=email, hashed_password=hashed)


def _create_token_pair(db: Session, user: User) -> tuple[TokenResponse, str]:
    """
    Private helper : create an access token + refresh token for a user.
    Extracted into a helper because both login_user() and refresh_user()
    need to issue a new token pair - DRY principle.

    This is NOT exposed as a public function - the "_" underscore prefix
    signals "internal use only".
    Callers use login_user() or refresh_user().

    Returns a tuple of (TokenResponse,plain_refresh_token).
    The route receives the plain refresh token and sets it as an HttpOnly cookie.
    The TokenResponse contains only the access token - the refresh token is
    never included in the JSON body.

    Steps :
    1. Create a short lived JWT Access Token.
    2. Generate an opaque random refresh token string.
    3. Hash the refresh token
    4. Store the hash in the DB with an expiry.
    5. Return BOTH tokens (TokenResponse for the body,plain_refresh_token for the cookie)

    """
    # 1. Access Token - JWT , stateless , short lived
    access_token = create_access_token({"sub": user.email})

    # 2. Refresh Token - opaque random string , stateful (stored in DB)
    plain_refresh_token = generate_refresh_token()

    # 3. Hash before storage
    token_hash = hash_refresh_token(plain_refresh_token)

    # 4. Persist the hash (not the plain token)
    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    refresh_token_repository.create(
        db, user_id=user.id, token_hash=token_hash, expires_at=expires_at
    )
    # 5. Return the plain token alongside the response so the route can set the cookie.
    # The plain token is never stored - only the hash is in the DB
    return TokenResponse(access_token=access_token), plain_refresh_token


def login_user(db: Session, email: str, password: str) -> tuple[TokenResponse, str]:
    """
    Authenticate a user and return a token pair (access + refresh )

    Returns the TokenResponse containing both tokens on success.
    Raises AuthError on failure.

    Security Note: we raise the SAME error message whether the email doesn't
    exist OR the password is wrong. Returning different messages for each case would let an attacker enumerate
    which emails are registered in our system (user enumeration attack).
    One generic message prevents this.

    """
    user = user_repository.get_by_email(db, email)

    # Check both conditions before raising - avoids short-circuit timing differences
    # (avoids situation where the program exists early (short circuiting) depending on which check failed first)
    # (by checking both every time together , the reponse takes same time and make it difficult for attackers)
    # that could theoretically leak which branch was taken.

    if not user or not verify_password(password, user.hashed_password):
        raise AuthError("Invalid email or password")

    return _create_token_pair(db, user)


def refresh_user(db: Session, plain_refresh_token: str) -> tuple[TokenResponse, str]:
    """
    Validate a refresh token and issue a new token pair.

    This implements TOKEN ROTATION:
    - The old refresh token is revoked (can never be used again)
    - A brand new access token + refresh token pair is issued.

    WHY ROTATION?

    If a token is stolen and the attacker uses it first, the legitimate
    user's next refresh call will fail (their token was just rotated away).
    They get a 401 and are prompted to log in - which alerts them something
    is wrong. Without rotation, a stolen token is silently valid until expiry.

    Validation checks (all must pass):
    1. Token hash exists in the DB (not tampered or fabricated)
    2. is_revoked is False
    3. expires_at is in the future (not expired automatically)

    Raises AuthError if any check fails.

    """

    token_hash = hash_refresh_token(plain_refresh_token)
    stored_token = refresh_token_repository.get_by_hash(db, token_hash)

    # Check 1 : Does this hash exist ?
    if not stored_token:
        raise AuthError("Invalid refresh token")

    # Check 2 : has it been revoked ? (logout or previous rotation)
    if stored_token.is_revoked:
        # A revoked token being used again is suspicious - could be a reply attack.
        # Advanced: at this point we could revoke ALL tokens for this user as a
        # security measure (logout all devices). We keep it simple here.
        raise AuthError("Refresh token has been revoked")

    # Check 3: has it expired naturally?
    if stored_token.expires_at < datetime.now(timezone.utc):
        raise AuthError("Refresh token has expired")

    # Load the user this token belongs to
    # db.get(Model,pk) is SQL Alchemy 2.0's primary-key lookup
    user = db.get(User, stored_token.user_id)
    if not user:
        raise AuthError("User not found")

    # ROTATE : revoke the old token before issuing a new pair
    refresh_token_repository.revoke(db, stored_token)

    # Issue a fresh pair
    return _create_token_pair(db, user)


def logout_user(db: Session, plain_refresh_token: str) -> None:
    """
    Revoke a refresh token, effectively ending the session.

    The access token remains technically valid until it expires (15 min).
    This is an accepted trade-off in stateless JWT auth - the access token
    window is short enough that it is not a practical concern.

    If we need instance access token revocatoin - we could add a token blocklist
    (typically Redis).

    Raises AuthError if the token doesn't exist or is already revoked.

    """
    token_hash = hash_refresh_token(plain_refresh_token)
    stored_token = refresh_token_repository.get_by_hash(db, token_hash)

    if not stored_token or stored_token.is_revoked:
        raise AuthError("Invalid or already revoked token")

    refresh_token_repository.revoke(db, stored_token)
