from datetime import date, datetime

from pydantic import BaseModel,Field

class MovieCreate(BaseModel):
    """ 
    Payload for POST /movies

    All fields are required - we must provide everything to create a movie

    """

    title:str
    description: str | None = None
    duration_minutes: int = Field(gt=0) # gt=0 means greater than 0 - Pydantic rejects 0 or negative
    language:str
    release_date:date  # Pydantic parses "2024-06-15" strings into a date object automatically


class MovieUpdate(BaseModel):
    """ 
    Payload for PUT /movies/{id}

    Every field is optional - the client only sends what they want to change.
    Fields not included in the request body are left unchanged in the DB.

    This works because the service calls .model_dump(exclude_unset=True),
    which returns only the fields that are explicitly provided in the request,
    not all fields (including the None defaults).

    """
    title:str | None = None 
    description: str | None = None
    duration_minutes: int | None = Field(default=None,gt=0)
    language:str | None = None
    release_date:date | None = None
    is_active: bool | None = None 


class MovieResponse(BaseModel):
    """ 
    Returned for every movie endpoint - GET, POST, PUT

    Includes the full set of columns including server-generated ones 
    (id, created_at,updated_at) so the client always has the complete picture.

    model_config from attributes : tells Pydantic to read values from 
    SQLAlchemy model attributes (ORM Objects) not just plain dicts.
    Same as we did for the UserResponse.

    """
    
    id:int
    title:str 
    description: str | None 
    duration_minutes: int 
    language:str 
    release_date:date
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes":True} # tells Pydantic to read data from object attributes (like SQLAlchemy ORM models) instead of expecting a dictionary.

    