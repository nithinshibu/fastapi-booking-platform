from sqlalchemy import Boolean,String
from sqlalchemy.orm import Mapped,mapped_column

from app.models.base import BaseModel

class User(BaseModel):
    """ 
    Maps to the 'users' table in PostgreSQL.

    Inherits id,created_at,updated_at from the BaseModel.
    We never store the plain password - only the hashed version.

    """

    __tablename__ = "users"

    email:Mapped[str] = mapped_column(String,unique=True,nullable=False,index=True)
    hashed_password:Mapped[str] = mapped_column(String,nullable=False)
    is_active:Mapped[bool] = mapped_column(Boolean,default=True,nullable=False)