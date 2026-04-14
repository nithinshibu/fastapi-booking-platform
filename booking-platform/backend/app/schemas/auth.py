from pydantic import BaseModel,EmailStr,Field

# Schemas are our DTOs (Data Transfer Objects).
# They define the shape of data coming IN to our API (requests)
# and going OUT (responses). They are NOT our database models.

# .NET equivalent : our Request/Response record classes or ViewModels.

# Pydantic validates every field automatically when a request arrives - 
# wrong type,missing field, or failed constraint = 422 Unprocessable Entity,
# with a detailed error body. We write zero validation code ourself.

# Key rule: schemas live in app/schemas/, models live in app/models.
# Never return a SQLAlchemy model object directly from a route - always 
# convert to a schema first. This controls exactly what data leaves our API.

class RegisterRequest(BaseModel):
    """ 
    Payload for POST /auth/register.

    EmailStr validates the format of the email (requires the email-validator package).
    Field(min_length=8) rejects passwords shorter than 8 characters before
    our code even runs - Pydantic handles the 422 response automatically. 
      
    """

    email:EmailStr
    password:str = Field(min_length=8)


class LoginRequest(BaseModel):
    """ Payload for POST /auth/login """
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    """ 
    Returned after a successful registration.

    We never include hashed_password here - the schema acts as a whitelist,
    so only fields we explicitly declare can ever leak our of our API.
    This is safer than trying to remember to exclude sensitive fields manually.

    """

    id:int
    email:str

    # model_config tells Pydantic it's OK to build this from a SQLAlchemy
    # model object (not just a plain dict).
    # Without this , Pydantic would refuse to read attributes off an ORM instance.

    # .NET equivalent: AutoMapper mapping from User entity -> UserResponse DTO.
    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """
    Returned after a successful login.

    Now contains BOTH tokens:
    - access_token  ->  short-lived JWT (15 min),sent on every API request.
    - refresh_token ->  long lived opaque string (7 days) used only to get
                        a new access_token when the current one expires.
    
    The frontend stores both. The access token goes in the Authorization header.
    The refresh token is stored securely and only used at /auth/refresh.

    'token_type: bearer' is the OAuth2 standard - client must send the token
    in the Authorization header as : Bearer <access_token> 

    """
    access_token:str
    refresh_token:str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    """ 
    Payload for POST /auth/refresh and POST /auth/logout

    The client sends back the refresh token it received at login.
    The server validates it, then either issues new tokens (refresh)
    or revokes it (logout).

    """
    refresh_token : str
