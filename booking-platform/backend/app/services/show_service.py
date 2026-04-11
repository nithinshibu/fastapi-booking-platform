from sqlalchemy.orm import Session

from app.models.show import Show
from app.repositories import movie_repository,show_repository
from app.schemas.show import ShowCreate
from app.services.movie_service import MovieNotFoundError

def get_shows_for_movie(db:Session,movie_id:int) -> list[Show]:
    """ 
    Return all shows for a movie.
    Validates the movie exists first - no point querying shows for a ghost movie.
    Raises MovieNotFoundError if the movie doesn't exist (route converts to 404).

    """
    
    if movie_repository.get_by_id(db,movie_id) is None:
        raise ModuleNotFoundError(f"Movie with id {movie_id} not found")
    return show_repository.get_by_movie(db,movie_id)


def create_show(db:Session,payload:ShowCreate) -> Show:
    """
    Create a new show for a movie.

    Business rules enforced here:
        1. The movie must exist - we validate the movie_id before inserting.
        2. available seats is intialized to the total_seats - the client never sets this.
           It will be decremented automatically when the bookings are made.

    Raises MovieNotFoundError if the movie_id in the payload doesn't exist.

    """

    if movie_repository.get_by_id(db,payload.movie_id) is None:
        raise ModuleNotFoundError(f"Movie with id {payload.movie_id} not found")
    
    data = payload.model_dump()

    # Enforces the business rule : new shows start fully available.
    # The client sends total_seats - we derive available_seats from it.

    data["available_seats"] = data["total_seats"]

    return show_repository.create(db,data)