from datetime import datetime,timezone

from sqlalchemy import select,update
from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken

""" 

This repository follows the same pattern as user_repository.py:
pure DB operations , no business logic , no HTTP concerns.

The service layer calls these functions and decide what to do with
the results.
The repository just executes the SQL.

"""

def create(db:Session,*,user_id:int,token_hash:str,expires_at:datetime)-> RefreshToken:
    """ 
    Store a new refresh token row.
    We store the HASH, not the plain token - the plain token is only ever returned to the client
    in the HTTP response body and never persisted.

    """
    token = RefreshToken(user_id=user_id,token_hash=token_hash,expires_at=expires_at,is_revoked=False)
    db.add(token)
    db.commit()
    db.refresh(token)
    return token

def get_by_hash(db:Session,token_hash:str) -> RefreshToken | None:
    """ 
    Look up a refresh token by its SHA-256 hash.

    Called on every /auth/refresh and /auth/logout request.
    The index on token_hash makes this a fast single-row lookup.

    Returns None if the hash is not found (invalid or tampered token).

    """
    statement = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
    return db.execute(statement).scalar_one_or_none()

def revoke(db:Session,token:RefreshToken) -> None:
    """ 
    Mark a single refresh token as revoked.

    We UPDATE is_revoked to True rather than deleting the row.
    Why? Keeping the row let us detect "token reuse attacks":
    if a revoked token is used again,we know something suspicious happened
    and can alert the user or force a full logout.

    Called during:
    -Token rotation (old token revoked, new one issued)
    -Explicit logout

    """
    token.is_revoked = True
    db.commit()

def revoke_all_for_user(db:Session,user_id:int)->None:
    """ 
    Revoke ALL active refresh tokens for a user in one query.

    Used for : "sign out of all devices" or security incident response.
    More efficient than loading each token and calling revoke() individually 
    - this issues a single UPDATE WHERE user_id=X.

    """
    db.execute(update(RefreshToken).where(RefreshToken.user_id==user_id,RefreshToken.is_revoked.is_(False)).values(is_revoked=True))
    db.commit()