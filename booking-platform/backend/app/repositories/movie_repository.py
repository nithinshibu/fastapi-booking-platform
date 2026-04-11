from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.movie import Movie

# Same pattern as user_repository - pure DB access , zero business logic
# Every function receives a Session and returns model instances or None

def get_all(db:Session) -> list[Movie]:
    """ 
    Return all movies ordered by release date descending (newest first).

    .NET equivalent: _context.Movies.OrderByDescending(m=>m.ReleaseDate).ToListAsync()
    """

    statement = select(Movie).order_by(Movie.release_date.desc())
    return list(db.execute(statement).scalars().all())

    # .scalars() unwraps the Row wrapper so we get Movie objects directly.
    # .all() executes and returns every result as a list.

def get_by_id(db:Session,movie_id:int) -> Movie | None:
    """ 
    Return a single movie by primary key or None if not found.

    """

    return db.get(Movie,movie_id)

    # db.get() is the SQLAlchemy 2.0 shorthand for lookup by primary key.
    # It also checks the session's identity map first (like EF Core's change tracker)
    # before hitting the DB - slightly more efficient than a full SELECT.


def create(db:Session,data:dict) -> Movie:
    """ 
    Insert a new movie row and return the fully populated Movie object.

    Accepts a plain dict so the repository stays decoupled from Pydantic schemas.
    The service is responsible for converting a schema into a dict before calling this.

    movie = Movie(**data) -> converts a dict into named parameters for the constructor.

    data = {
    "title": "Inception",
    "rating": 9
    }

    movie = Movie(**data) is equivalent to: movie = Movie(title="Inception", rating=9)

    """

    movie = Movie(**data)
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


def update(db:Session,movie:Movie,data:dict) -> Movie:
    """ 
    Apply a partial update to an existing movie and return the updated object.

    'data' contains only the fields to change (exclude_unset = True in the service 
    means untouched fields are never passed here).

    setattr(obj,key,value) is Python's way of dynamically setting an attribute by name
    - equivalent to : movie.title = data["title"] but works for any field.

    """
    for field, value in data.items():
        setattr(movie,field,value)
    db.commit()
    db.refresh(movie)
    return movie

def delete(db:Session, movie:Movie) -> None:
    """ 
    Permanently delete a movie row from the database. 
    
    """

    db.delete(movie)
    db.commit()


