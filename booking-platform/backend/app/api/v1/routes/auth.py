from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.dependencies.db import get_db
from app.schemas.auth import (
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.services.auth_service import (
    AuthError,
    login_user,
    logout_user,
    refresh_user,
    register_user,
)


# APIRouter is FastAPI's way of grouping related routes.
# Think of it like a Controller in .NET - all auth-related endpoints live here.

# prefix="/auth"    -> every route below is automatically prefixed, so
# def register(...) at path "/register" becomes POST /auth/register
# tags=["Auth"]     -> groups these routes under an "Auth" section in Swagger UI

router = APIRouter(prefix="/auth", tags=["Auth"])

# Cookie settings used on every set_cookie / delete_cookie call.
# Centralised here so login and refresh always use identical parameters -
# the browser matches cookies by name + path + domain + secure + samesite,
# so mismatched params on delete_cookie would silently fail to clear the cookie.

_COOKIE_KWARGS = dict(
    key="refresh_token", httponly=True, samesite="lax", path="/api/v1/auth"
)


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
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
        user = register_user(db, email=payload.email, password=payload.password)
        return user  # FastAPI uses response_model to serialize this automatically
    except AuthError as exc:
        # 400 Bad Request - the input was valid JSON but breaks a business rule
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/login", response_model=TokenResponse)
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticate a user and return the access token in the response body.

    Uses OAuth2PasswordRequestForm instead of a JSON Body.

    Why the change?

    The Swagger UI "Authorize" button and the OAuth2 standard both send
    credentials as form data (application/x-www-form-urlencoded),not JSON.
    OAuth2PasswordRequestForm is FastAPI's built-in handler for that format.

    The refresh token is set as an HttpOnly cookie - it is NOT in the json body.
    The browser stores and sends it automatically;
    Javascript cannot read it:

    Response body:
            access_token - short lived JWT,attach to every API request.
            token_type - bearer (OAuth2 standard)

    Set-Cookie header:
            refresh_token - long lived opaque token, HttpOnly, SameSite=Lax

    On Failure : returns 401 Unauthorized

    """

    try:
        token_response, plain_refresh_token = login_user(
            db, email=form_data.username, password=form_data.password
        )
        response.set_cookie(
            **_COOKIE_KWARGS,
            value=plain_refresh_token,
            secure=settings.COOKIE_SECURE,
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86_400,
        )
        return token_response

    except AuthError as exc:
        # 401 Unauthorized - credentials are wrong or user doesn't exist
        # WWW-Authenticate header is the OAuth2 standard signal to the client
        # that Bearer token authentication is required/failed
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/refresh", response_model=TokenResponse)
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Exchange the refresh token cookie for a new access token + rotated refresh token.

    TOKEN Rotation happens here:
    - The submitted refresh token is REVOKED.
    - A brand new token pair is issued (new access token in body , new refresh cookie).

    This endpoint is called automatically by the frontend when the access token expires (typically
    a 401 response triggers a slient refresh attempt).
    The user never sees this - it happens in the Axios response interceptor.

    Returns 401 if the cookie is missing,revoked or expired.
    Returns 200 with a new TokenResponse on success.

    """

    plain_refresh_token = request.cookies.get("refresh_token")
    if not plain_refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        token_response, new_plain_refresh_token = refresh_user(
            db, plain_refresh_token=plain_refresh_token
        )
        response.set_cookie(
            **_COOKIE_KWARGS,
            value=new_plain_refresh_token,
            secure=settings.COOKIE_SECURE,
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86_400,
        )
        return token_response
    except AuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Revoke the refresh token cookie, ending the session server-side.

    Returns 204 No Content on success - no body needed, the action is complete.

    The cookie is always cleared in the response , even if the token was already
    revoked or the cookie was absent - so the client ends up logged out regardless.

    Why 204 and not 200 ?

    200 means "Here is some content in response to your request"
    204 means "Done - nothing to return". Logout has no meaningful response body.
    This is the REST Standard for operations that succeed with no content.

    The frontend should also clear its locally stored tokens after calling this.

    Note :
    The access token (JWT) remains technically valid until it expires in ~15 mins. This
    is an accepted trade-off, instant revocation would require a Redis block list.

    """
    plain_refresh_token = request.cookies.get("refresh_token")
    if plain_refresh_token:
        try:
            logout_user(db, plain_refresh_token=plain_refresh_token)
        except AuthError:
            # Be lenient on logout - if the token is already gone, that is fine.
            # The user's intent (end the session) is effectively achieved either way
            pass

    # Always delete the cookie. Must pass the same path/httponly/secure/samesite
    # that were used setting it - otherwise the browser won't match it.
    response.delete_cookie(**_COOKIE_KWARGS, secure=settings.COOKIE_SECURE)
