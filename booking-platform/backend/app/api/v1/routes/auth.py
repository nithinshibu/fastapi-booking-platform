from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.auth import (
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.services.auth_service import (
    AuthError,
    login_user,
    logout_user,
    refresh_user,
    register_user,
)


# APIRouter is FastAPI's way of grouping related routes.
# Think of it like a Controller in .NET - all auth-related endpoints live here.

# prefix="/auth"    -> every route below is automatically prefixed, so
# def register(...) at path "/register" becomes POST /auth/register
# tags=["Auth"]     -> groups these routes under an "Auth" section in Swagger UI

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user account.

    FastAPI reads 'payload:RegisterRequest' and automatically:
        1. Parses the incoming JSON body
        2. Validates it against RegisterRequest (email format, password length)
        3. Returns 422 with details if the validation fails - before our code runs

    'db:Session=Depends(get_db)' is Dependency Injection.

    .NET equivalent: constructor injection of IAppDbContext.
    FastAPI resolves get_db() per-request and closes the session after.

    'response_model=UserResponse' tells FastAPI to:
        1. Validate the return value against the UserResponse
        2. Strip any fields not in UserResponse (hashed_password never leaks)
        3. Generate the correct response schema in Swagger UI.

    """

    try:
        user = register_user(db, email=payload.email, password=payload.password)
        return user  # FastAPI uses response_model to serialize this automatically
    except AuthError as exc:
        # 400 Bad Request - the input was valid JSON but breaks a business rule
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Authenticate a user and return BOTH tokens.

    Uses OAuth2PasswordRequestForm instead of a JSON Body.

    Why the change?

    The Swagger UI "Authorize" button and the OAuth2 standard both send
    credentials as form data (application/x-www-form-urlencoded),not JSON.
    OAuth2PasswordRequestForm is FastAPI's built-in handler for that format.

    Response now contains:
            access_token - short lived JWT,attach to every API request.
            refresh_token - long lived opaque string, stored securely, we use only at /refresh
            token_type - bearer (OAuth2 standard)

    On Failure : returns 401 Unauthorized

    """

    try:
        return login_user(db, email=form_data.username, password=form_data.password)

    except AuthError as exc:
        # 401 Unauthorized - credentials are wrong or user doesn't exist
        # WWW-Authenticate header is the OAuth2 standard signal to the client
        # that Bearer token authentication is required/failed
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    """
    Exchange a valid refresh token for a new access token + new refresh token.

    TOKEN Rotation happens here:
    - The submitted refresh token is REVOKED.
    - A brand new token pair is issued.

    This endpoint is called automatically by the frontend when the access token expires (typically
    a 401 response triggers a slient refresh attempt).
    The user never sees this - it happens in the Axios response interceptor.

    Returns 401 if the token is invalid,revoked or expired.
    Returns 200 with a new TokenResponse on success.

    """
    try:
        return refresh_user(db, plain_refresh_token=payload.refresh_token)
    except AuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(payload: RefreshRequest, db: Session = Depends(get_db)):
    """
    Revoke the refresh token , ending the session server-side.

    Returns 204 No Content on success - no body needed, the action is complete.

    Why 204 and not 200 ?

    200 means "Here is some content in response to your request"
    204 means "Done - nothing to return". Logout has no meaningful response body.
    This is the REST Standard for operations that succeed with no content.

    The frontend should also clear its locally stored tokens after calling this.

    Note :
    The access token (JWT) remains technically valid until it expires in ~15 mins. This
    is an accepted trade-off, instant revocation would require a Redis block list.

    """
    try:
        logout_user(db, plain_refresh_token=payload.refresh_token)
    except AuthError:
        # Be lenient on logout - if the token is already gone, that is fine.
        # The user's intent (end the session) is effectively achieved either way
        pass
