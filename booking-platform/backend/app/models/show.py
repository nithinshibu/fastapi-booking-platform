from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime,ForeignKey,Integer,String
from sqlalchemy.orm import Mapped,mapped_column,relationship

from app.models.base import BaseModel

# Only used by: IDE autocomplete,static type checkers and without this? You’d get: ImportError: circular import
if TYPE_CHECKING:
    from app.models.movie import Movie

class Show(BaseModel):
    """ 
    Maps to the 'shows' table in PostgreSQL.

    A Show is one specific screening of a Movie at a given time and hall.

    One Movie -> Many Shows (one to many relationship)
    
    """

    __tablename__ = "shows"

    # ForeignKey creates the DB-level constraint : this columns must contain
    # a value that exists in movies.id . PostgreSQL enforces this - inserting 
    # a show with a non-existent movie_id will raise an IntegrityError.

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id",ondelete="CASCADE"),index=True)

    # ondelete="CASCADE" means : if a Movie is deleted , all its shows are 
    # automatically deleted too. Without this , deleting a movie with shows 
    # would raise a foreign key violation error.

    # The datetime of this specific screening - stored with timezone info.

    show_time: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,index=True)

    # Total seats in the hall - set at creation and never changes 
    total_seats: Mapped[int] = mapped_column(Integer,nullable=False)

    # Seats still available for booking - starts equal to total_seats.
    # Decremented each time a booking is made.
    # Keeping this as a column (denormalized) avoids a COUNT query on bookings
    # everytime someone checks seat availability.

    available_seats: Mapped[int] = mapped_column(Integer,nullable=False)

    hall_name: Mapped[str] = mapped_column(String,nullable=False)

    # Relationship - Python level navigation to the parent Movie.
    # Lets you do : show.movie.title without writing  a JOIN .
    # back_populates = "shows" must match the attribute name on Movie.

    movie : Mapped[Movie] = relationship("Movie",back_populates="shows")