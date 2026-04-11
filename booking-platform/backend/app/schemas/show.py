from datetime import datetime

from pydantic import BaseModel,Field

class ShowCreate(BaseModel):
    """ 
    Payload for POST /shows

    Note: available_seats is NOT here - it is set automatically by the service to equal total_seats.
    The client should NEVER control the seat availability directly.

    """

    movie_id:int
    show_time:datetime
    total_seats: int = Field(gt=0)
    hall_name: str

class ShowResponse(BaseModel):
    """ Returned for every show endpoint. """

    id:int
    movie_id:int
    show_time:datetime
    total_seats:int
    available_seats:int
    hall_name:str
    created_at:datetime
    updated_at:datetime

    model_config = {"from_attributes": True}

