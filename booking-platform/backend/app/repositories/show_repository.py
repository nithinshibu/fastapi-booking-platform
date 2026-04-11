from sqlalchemy import select 
from sqlalchemy.orm import Session

from app.models.show import Show

def get_by_movie(db:Session,movie_id:int) -> list[Show]:
    """ 
    Return all shows for a given movie , ordered by show_time ascending 
    (next showing first).   

    """

    statement = (select(Show).where(Show.movie_id == movie_id).order_by(Show.show_time.asc()))

    return list(db.execute(statement).scalars().all())


def create(db:Session, data:dict) -> Show:
    """ Insert a new show row and return the fully populated Show object """

    show = Show(**data)
    db.add(show)
    db.commit()
    db.refresh(show)
    return show