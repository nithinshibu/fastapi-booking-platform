from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.schemas.movie import MovieCreate,MovieResponse,MovieUpdate
from app.services.movie_service import MovieNotFoundError, create_movie,delete_movie,get_all_movies,get_movie,update_movie


router = APIRouter(prefix="/movies",tags=["Movies"])

@router.get("",response_model=list[MovieResponse])
def list_movies(db:Session = Depends(get_db)):
    """ 
    Return all movies. No authentication required - anyone can browse movies.

    response_model=list[MovieResponse] tells FastAPI to serialize a Python list of Movie
    ORM objects into a JSON Array of MovieResponse objects.    

    """
    return get_all_movies(db)

@router.get("/{movie_id}",response_model=MovieResponse)
def get_movie_by_id(movie_id: int,db:Session = Depends(get_db)):
    """ 
    Return a single movie by id. No authentication required.

    FastAPI automatically extracts 'movie_id' from the URL path and validates
    it is an integer - passing "abc" returns 422 before your code runs.

    .NET equivalent : [HttpGet("{id}")] with a route parameter.

    """
    try:
        return get_movie(db,movie_id)
    except MovieNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    

@router.post("",response_model=MovieResponse,status_code=status.HTTP_201_CREATED)
def create_new_movie(
    payload:MovieCreate,
    db:Session = Depends(get_db),
    _: object = Depends(get_current_user)  # enforces auth - user object not needed here
    ):
    """  
    
    Create a new movie. Authentication required.

    The "_" parameter is a convention for "I need this dependency to run
    (for its side effect of enforcing auth) but I don't use its return value."
    The user must be logged in, but we don't use their identity for anything here.
    
    """
    return create_movie(db,payload)


@router.put("/{movie_id}",response_model=MovieResponse)
def update_existing_movie(movie_id:int,payload:MovieUpdate,db:Session = Depends(get_db),_:object = Depends(get_current_user)):
    """ 
    Partially update a movie. Authentication required
    Only fields included in the request body are updated - others are left unchanged.

    """
    try:
        return update_movie(db,movie_id,payload)
    except MovieNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(exc))
    
@router.delete("/{movie_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_movie(movie_id:int,db:Session=Depends(get_db),_:object = Depends(get_current_user)):
    """ 
    Delete a movie permanently. Authentication required.

    Returns 204 No Content on success - the standard HTTP response for a successful DELETE. There is no response body (nothing to return after deletion).

    .NET equivalent :  return NoContent();
    
    """

    try:
        delete_movie(db,movie_id)
    except MovieNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(exc))
