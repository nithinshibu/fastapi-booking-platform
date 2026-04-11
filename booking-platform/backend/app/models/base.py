from datetime import datetime
from sqlalchemy import DateTime,Integer,func
from sqlalchemy.orm import Mapped,mapped_column

from app.db.base import Base 

class BaseModel(Base):
    """ 
    Abstract base class shared by all models.
    Defines the common columns every table will have.

    Think of this as our abstract base entity class in .NET -
    all entities inherit Id,CreatedAt,UpdatedAt from it.

    __abstract__ = True tells SQLAlchemy NOT to create a table for this class itself.
    Only the concrete subclasses get tables.

    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(), # DB sets this automatically on INSERT
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(), 
        onupdate=func.now(), # DB updates this automatically on UPDATE
        nullable=False,
    )