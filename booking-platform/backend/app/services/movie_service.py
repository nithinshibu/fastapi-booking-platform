from sqlalchemy.orm import Session

from app.models.movie import Movie
from app.repositories import movie_repository
from app.schemas.movie import MovieCreate,MovieUpdate

class MovieNotFoundError(Exception):
    """ Raised when a requested movie doesnot exist in the database """
    pass

def get_all_movies(db:Session) -> list[Movie]:
    """ Return all movies. No business rules - straight pass-through to the repository """
    return movie_repository.get_all(db)


def get_movie(db:Session,movie_id:int)->Movie:
    """ 
    Return a single movie by id.
    Raises MovieNotFoundError if it doesn't exist - the route convert this to 404
    """

    movie = movie_repository.get_by_id(db,movie_id)
    if movie is None:
        return ModuleNotFoundError(f"Movie with id {movie_id} not found")
    return movie

def create_movie(db:Session,payload:MovieCreate)->Movie:
    """ 
    Create a new movie.

    model_dump() converts the Pydantic schema into a plain dict.
    We pass the dict to the repository so the repo stays schema-agnostic.

    """

    return movie_repository.create(db,payload.model_dump())


def update_movie(db:Session,movie_id:int,payload:MovieUpdate)->Movie:
    """ 
    Apply a partial update to a movie.

    model_dump(exclude_unset=True) is the key here - it returns only the fields
    the client actually sent , not all the fields including the None defaults.

    Without the exclude_unset=True , every field would be overwritten with None.
    
    """

    movie = get_movie(db,movie_id) # raises MovieNotFoundError if missing
    changes = payload.model_dump(exclude_unset=True)
    return movie_repository.update(db,movie,changes)


def delete_movie(db:Session,movie_id:int) -> None:
    """ Delete a movie permanently.Raises MovieNotFoundError if missing  """
    movie = get_movie(db,movie_id)
    movie_repository.delete(db,movie)