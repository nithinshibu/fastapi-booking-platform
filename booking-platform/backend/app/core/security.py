import hashlib
import secrets
from datetime import datetime,timedelta,timezone
from typing import Any

from jose import JWTError,jwt
from passlib.context import CryptContext

from app.core.config import settings

# CryptoContext is passlib's way of configuring which hashing algoritm to use.
# Think of this as setting up BCrypt.NET in .NET - bcrypt is intentionally slow
# making brute force attacks computationally expensive even if your DB leaks.
# "deprecated='auto'" means if your ever switch algorithms , old hashes are 
# automatically flagged for re-hashing on next login.

pwd_context = CryptContext(schemes=["bcrypt"],deprecated='auto')

def hash_password(plain_password:str) -> str:
    """ 
    Hash a plain-text password using bcrypt.

    .NET equivalent :  BCrypt.HashPassword(password)

    bcrypt embeds a random salt inside the hash string itself, so we never need to store the salt separately.
    Every call produces a different output even for the same input - that's intentional
    - (see verify_password for why?)

    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password:str,hashed_password:str) -> bool:
    """ 
    Compare a plain text password against a stored bcrypt hash.

    .NET equivalent : BCrypt.Verify(password,hash)

    You cannot reverse a bcrypt hash - passlib re-hashes the plain input with 
    the same embedded salt and compares. Also uses constant-time comparison internally
    to prevent the timing attacks (attacker can't guess chars one by one by measuring the 
    response time differences).

    """
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict[str,Any],expires_delta:timedelta | None = None) -> str:
    """ 
    Create a signed JWT access token.

    .NET equivalent : new JwtSecurityTokenHandler().WriteToken(new JwtSecurityToken(...))

    The 'data' dict becomes the JWT payload (claims). Typically we pass 
    {"sub":user_email} - 'sub' (subject) is the standard JWT claim for identity.

    We add 'exp' (expiry) automatically. python-jose validates 'exp' on decode, so expired tokens 
    are rejected without any extra code on our side.

    The token is signed with SECRET_KEY - anyone can read the payload (it's base64 , not encrypted),
    but they cannot forge or tamper with it without knowing the secret key. This is JWS (signed) , not JWE (encrypted).

    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode["exp"] = expire
    return jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)


def generate_refresh_token() -> str:
    """ 
    Generate a cryptographically secure random token string.
    secrets.token_urlsafe(64) produces a 64 random bytes encoded as URL-safe
    base64 - giving an 86 character string with ~512 bits of entropy.

    Why not a JWT for refresh tokens ?

    -   JWT are self validating => we don't need a DB lookup to verify them.
        That's great for access tokens (performance) but terrible for refresh tokens
        (we can't revoke them without a blocklist, which defeats the point).
    
    An opaque token MUST be looked up in the DB on every use. That lookup is what
    enables revocation - we just set is_revoked=True and the token is dead immediately.

    """
    return secrets.token_urlsafe(64)

def hash_refresh_token(token:str) -> str:
    """ 
    Hash a refresh token with SHA-256 before storing it in the database.

    WHY HASH?

    Same reason we hash passwords - defence in depth.
    If the database is ever read by an attacker (SQL injection, backup leak),
    they get hashes, not usable tokens. They cannot call /auth/refresh with a hash.

    Why SHA-256 (not bcrypt like passwords) ?
    -   Refresh tokens are already random (high entropy) - no need for a slow
        algorithm to defend against dictionary attacks. SHA-256 is fast and sufficient.
        bcrypt is slow BY DESIGN to restrict brute-force on low-entropy inputs (passwords).
        A 512 bits random token cannot be brute-forced regardless of algorithm speed.

    Returns a 64-character lowercase hex string.    

    """
    return hashlib.sha256(token.encode()).hexdigest()




def decode_access_token(token:str) -> dict[str,Any] | None:
    """ 
    Decode and validate a JWT.
    Returns the payload dict , or None if invalid.

    .NET equivalent : JWTSecurityTokenHandler.ValidateToken(...)

    python-jose automatically validates:
        - Signature -> tampered tokens are rejected
        - Expiry -> expired tokens raise JWTError (we catch and return None)
        - Algorithm -> tokens signed with a different algorithm are rejected

    We return None instead of raising , so callers get a clean boolean-style
    result. The HTTP 401 decision happens one layer up in the dependency(get_current_user),
    not here. Security logic stays in security.py;
    HTTP concerns stay in dependencies.
      
    """
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None