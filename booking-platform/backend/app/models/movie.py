from __future__ import annotations
from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy import Boolean,Integer,String
from sqlalchemy.orm import Mapped,mapped_column,relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.show import Show


class Movie(BaseModel):
    """ 
    Maps to the 'movies' table in PostgreSQL.
    Inherits id, created_at,updated_at from BaseModel.

    """

    __tablename__ = "movies"

    # index=True tells the database to create an index on this column for faster queries.

    title: Mapped[str] = mapped_column(String,nullable=False,index=True)

    # Text() would also work for long strings , but String is fine here.
    # nullable= True means the column allows NULL - description is optional.

    description: Mapped[str | None] = mapped_column(String,nullable=True)

    duration_minutes: Mapped[int] = mapped_column(Integer,nullable=False)

    language: Mapped[str] = mapped_column(String,nullable=False)

    # SQLAlchemy maps Python's data type to PostgreSQL's DATE column.
    # We store just the data (no time), which is appropriate for the release dates.
    release_date: Mapped[date] = mapped_column(nullable=False)

    # is_active lets us hide movies from listings without deleting them.
    # This is called a "soft disable" - useful when a movie is taken off schedule 
    # but we don't want to lose it data or break foreign keys in bookings.

    is_active: Mapped[bool] = mapped_column(Boolean,default=True,nullable=False)

    # Relationship - the Python-level link to all Show rows for this movie.
    # SQLAlchemy loads these lazily by default (only when we access .shows) .
    # back_populates="movie" tells SQLAlchemy that Show.movie points back here.
    # Type_CHECKING import above avoids a circular import at runtime while still
    # giving type checkers (and IDE) full awareness of the Show type.

    shows: Mapped[list[Show]] = relationship("Show",back_populates="movie")