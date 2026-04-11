from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.schemas.show import ShowCreate,ShowResponse
from app.services.movie_service import MovieNotFoundError
from app.services.show_service import create_show,get_shows_for_movie

# No prefix here  - the two endpoint have different URL structures:
# GET  /movies/{movies_id}/shows  (nested under movies)
# POST /shows                     (top level)
# Defining full paths explicitly is cleaner than trying to share a prefix.

router = APIRouter(tags=["Shows"])

@router.get("/movies/{movie_id}/shows",response_model=list[ShowResponse])
def list_shows_for_movie(movie_id:int,db:Session = Depends(get_db)):
    """ 

    Return all shows for a specific movie , ordered by the show_time in ascending order.
    No authentication required.

    The nested URL /movies/{movie_id}/shows follows REST conventions for 
    sub-resources - shows belongs to a movie, so they live under it in the URL. 
      
    """
    try:
        return get_shows_for_movie(db,movie_id)
    except MovieNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(exc))
    

@router.post("/shows",response_model=ShowResponse,status_code=status.HTTP_201_CREATED)
def create_new_show(payload:ShowCreate,db:Session = Depends(get_db),_: object = Depends(get_current_user)):
    """ 
    Create a new show. Authentication required.
    The movie_id in the request body must reference an existing movie.
    available_seats is set automatically - do not include it in the request.
    """
    try:
        return create_show(db,payload)
    except MovieNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(exc))