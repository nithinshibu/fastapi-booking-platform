from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.auth import LoginRequest,RegisterRequest,TokenResponse,UserResponse
from app.services.auth_service import AuthError,login_user,register_user


# APIRouter is FastAPI's way of grouping related routes.
# Think of it like a Controller in .NET - all auth-related endpoints live here.

# prefix="/auth"    -> every route below is automatically prefixed, so
# def register(...) at path "/register" becomes POST /auth/register
# tags=["Auth"]     -> groups these routes under an "Auth" section in Swagger UI

router = APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register(payload:RegisterRequest,db:Session=Depends(get_db)):
    """  
    Register a new user account.

    FastAPI reads 'payload:RegisterRequest' and automatically:
        1. Parses the incoming JSON body
        2. Validates it against RegisterRequest (email format, password length)
        3. Returns 422 with details if the validation fails - before our code runs

    'db:Session=Depends(get_db)' is Dependency Injection.

    .NET equivalent: constructor injection of IAppDbContext.
    FastAPI resolves get_db() per-request and closes the session after.

    'response_model=UserResponse' tells FastAPI to:
        1. Validate the return value against the UserResponse
        2. Strip any fields not in UserResponse (hashed_password never leaks)
        3. Generate the correct response schema in Swagger UI.
    
    """

    try:
        user = register_user(db,email=payload.email,password=payload.password)
        return user  # FastAPI uses response_model to serialize this automatically
    except AuthError as exc:
        # 400 Bad Request - the input was valid JSON but breaks a business rule
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(exc))


@router.post("/login",response_model=TokenResponse)
def login(payload:LoginRequest,db:Session=Depends(get_db)):
    """ 
    Authenticate a user and return a JWT Access Token.

    On Success : returns {"access_token":"...","token_type":"bearer"}
    On Failure : returns 401 Unauthorized

    The client must store this token and send it on every protected request:
        Authorization: Bearer <access_token>
    """

    try:
        token = login_user(db,email=payload.email,password=payload.password)
        return TokenResponse(access_token=token)
    except AuthError as exc:
        # 401 Unauthorized - credentials are wrong or user doesn't exist
        # WWW-Authenticate header is the OAuth2 standard signal to the client
        # that Bearer token authentication is required/failed
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=str(exc),headers={"WWW-Authenticate":"Bearer"})