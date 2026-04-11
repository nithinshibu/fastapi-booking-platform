from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.dependencies.db import get_db
from app.models.user import User 
from app.repositories import user_repository

# OAuth2PasswordBearer does two things:
#       1. At runtime: extracts the raw token string from the incoming request's
#                      "Authorization: Bearer <token>" header. If the header is missing,
#                      FastAPI automatically returns 401 before even our code runs.
#       2. In Swagger UI : the tokenUrl tells the "Authorize" button where to send login credentials
#                          so we can test protected routes interactively in /docs.
# 
# .NET equivalent: 
#       services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
#               .AddJwtBearer(options=> options.TokenValidationParameters = ...)
# 
# The tokenUrl must match the actual login route we registered in the main.py.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(get_db)) -> User:
    """ 
    FastAPI dependency that validates a JWT and returns the authenticated User.

    .NET equivalent : the combination of [Authorize] on a controller +
    reading HTTPContext.User inside the action - except here , the full resolution
    chain is explicit and readable.

    This function is NEVER called directly by our code.
    FastAPI sees Depends(get_current_user) on a route and calls it automatically
    before the route handler runs - just like middleware, but scoped to 
    individual routes instead of the whole pipeline.

    Resolution Chain :
            1. OAuth2PasswordBearer pulls the raw token from the Authorization header
               (FastAPI returns 401 automatically if the header is absent)
            2. decode_access_token() validates the signature + expiry -> returns payload or None
            3. We extract 'sub' (the user's email) from the payload
            4. We load the User row from the DB by email
            5. We return the User -> the route receives it as an injected argument
    
    Any failure at steps 2-4 raises, the same generic 401 - we never reveal whether the token
    was expired , tampered or the user was deleted.
      
    """

    # Define once , reuse - avoids repeating the same HTTPException in every branch

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})

    # Step 1 : decode and validate the JWT 
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    #Step 2 : extract the subject claim (email) we set in create_access_token()
    email: str | None = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    # Step 3 : confirm the user still exists in the DB 
    # This catches the edge case like "token is valid but the account was deleted"
    user = user_repository.get_by_email(db,email)
    if user is None:
        raise credentials_exception
    
    return user