from sqlalchemy.orm import Session

from app.core.security import create_access_token,hash_password,verify_password
from app.models.user import User
from app.repositories import user_repository

# The service layer is where the business logic lives.
# It sits between the route (HTTP Layer) and the repository (DB Layer)

# .NET equivalent : our UserService / AuthService class.

# Rules this layer owns:
#           - Is this email already taken ?
#           - Are those credentials valid ?
#           - What do we return on sucess ?

# Rules this layer does NOT owns:
#           - How to hash passwords             -> handles this in security.py
#           - How to read / write into the DB   -> handles this in the user_repository.py
#           - How to format the HTTP reponse    -> handled in the route

class AuthError(Exception):
    """ 
    Raised when authentication or registration fails for a known business reason.

    Using a custom exception type instead of returning None or a bool means 
    the route can catch it and decide the HTTP status code - the service itself
    stays HTTP-agnostic (The code is independent of HTTP details (like status codes or requests) and focuses only on business logic.).
    This follows the same pattern as throwing a custom domain exception in .NET and catching it in a controller action filter.

    """
    pass



def register_user(db:Session,email:str,password:str) -> User:
    """ 
    Register a new user account.

    Business rules enforced here:
    1. Email must not already exist in the DB.
    2. Password is hashed before it reaches the repository - plaintext never touches the database layer.

    Returns the newly created User on success.
    Raises AuthError if the email is already registered.

    """
    existing_user = user_repository.get_by_email(db,email)
    if existing_user:
        raise AuthError("Email already registered")
    
    hashed = hash_password(password)
    return user_repository.create(db,email=email,hashed_password=hashed)


def login_user(db:Session,email:str,password:str) -> str:
    """ 
    Authenticate a user and return a signed JWT access token. 

    Returns the token string on success.
    Raises AuthError on failure.

    Security Note: we raise the SAME error message whether the email doesn't
    exist OR the password is wrong. Returning different messages for each case would let an attacker enumerate
    which emails are registered in our system (user enumeration attack).
    One generic message prevents this.
      
    """
    user = user_repository.get_by_email(db,email)

    # Check both conditions before raising - avoids short-circuit timing differences
    # (avoids situation where the program exists early (short circuiting) depending on which check failed first)
    # (by checking both every time together , the reponse takes same time and make it difficult for attackers)
    # that could theoretically leak which branch was taken.

    if not user or not verify_password(password,user.hashed_password):
        raise AuthError("Invalid email or password")
    
    # 'sub' (subject) is the standard JWT claim for identifying the principal.
    # We use email here , later we will decode this to load the current user.

    return create_access_token({"sub":user.email})
