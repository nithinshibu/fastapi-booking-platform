from fastapi import APIRouter,Depends

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.auth import UserResponse

router = APIRouter(prefix="/users",tags=["Users"])


@router.get("/me",response_model=UserResponse)
def get_me(current_user:User = Depends(get_current_user)):
    """ 
    Returns the currently authenticated user's profile.

    Depends(get_current_user) is the entire auth guard.
    FastAPI resolves it before this function runs:
        - No Token          -> 401 (returned by OAuth2PasswordBearer automatically)
        - Invalid Token     -> 401 (raised inside get_current_user)
        - Valid Token       -> current_user is populated and passed in here

    
    .NET equivalent:
    [Authorize]
    [HttpGet("me")]
    public IActionResult GetMe() => Ok(currentUser);

    The route handler itself is intentionally trivial - all the auth logic lives in the get_current_user,
    making it reusable across every protected route we add in future.        
    
    """
    return current_user