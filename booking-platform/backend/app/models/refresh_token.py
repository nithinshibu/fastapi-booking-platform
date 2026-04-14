from datetime import datetime

from sqlalchemy import Boolean,DateTime,ForeignKey,String
from sqlalchemy.orm import Mapped,mapped_column,relationship

from app.models.base import BaseModel

class RefreshToken(BaseModel):
    """ 
    Represents one active session for a user.

    Why a separate table (not a column on User) ?
        - A user can have many active sessions - phone , laptop , work PC etc.
        - A column on User can hold only ONE value. 
        - A separate table holds one per session, so we can revoke a single device without
        - logging out every other device.
    
    This is the same pattern as .NET Identity's RefreshTokens Table.

    Key Design Decisions :

        1. We store token_hash, not the plain token.
           If our database is ever compromised, the attacker gets hashes-
           useless without the original token. The plain token only ever exists in memory and in the 
           HTTP response body.
        
        2. is_revoked + expires_at together define validity.
           A token is valid only when Both conditions are TRUE:
                - is_revoked is FALSE
                - expires_at is in the future
           Having both lets us revoke a token early (logout) and let tokens
           expire naturally without running cleanup jobs.
        
        3. ondelete="CASCADE" means deleting a User automatically deletes all their refresh tokens.
           No orphaned rows.
        

    """

    __tablename__ = "refresh_tokens"

    # Foreign key to the user who owns this token.
    # index=True because we sometimes query "revoke all tokens for user X".
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id",ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # SHA-256 hash of the opaque token string.
    # unique = True + index = True : we look up tokens by hash on every /refresh call
    # so this needs to be fast. Unique ensures no two sessions share a hash.
    token_hash: Mapped[str] = mapped_column(
        String(64), # SHA-256 produces a 64 character hex string
        nullable=False,
        unique=True,
        index=True
    )

    # When this token expires - set to now() + REFRESH_TOKEN_EXPIRE_DAYS on creation.
    # timezone=True stores as UTC in PostgreSQL (TIMESTAMPTZ column).
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    # Explicitly revoked by a logout call or a token rotation.
    # We keep the row (not delete it) so we can detect token reuse:
    # If someone tries to use an already-revoked token, that is a red flag
    # that the token may have been stolen - we could trigger a full logout
    # of all sessions as a security response 
    is_revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    
