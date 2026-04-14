from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """ 
    Application configuration loaded from the .env file.

    Think of this as your appsettings.json in a dotnet project  , bound to a typed class (IOptions<T>).

    Pydantic validates each value on startup - 
    if the DATABASE_URL is missing , then the app wouldn't start, which is exactly the behavior we want.

    """

    DATABASE_URL:str
    SECRET_KEY:str
    ALGORITHM:str = "HS256"


    """ 

    With refresh token in place, keep access token SHORT (15 mins)
    Short lived access tokens limit damage if one is intercepted -
    an attacker only has a 15-min window.
    The refresh token quietly issues a new access token before it expires , so users never notice.

    """
    ACCESS_TOKEN_EXPIRE_MINUTES: int =30

    """ 
    Refresh token live much longer - 7 days is the common default.
    Each time the token is used it is ROTATED (new one issued and old revoked),
    so an active user effectively never gets logged out.
    An idle user (hasn't opened the app in 7 days) must log in again.

    """
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ".env"


# Single shared instance - import this everywhere when we need config.
# Never call os.getenv() directly in our code , always use settings.FIELD_NAME.

settings = Settings()