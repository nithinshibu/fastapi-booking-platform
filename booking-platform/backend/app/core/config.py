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
    ACCESS_TOKEN_EXPIRE_MINUTES: int =30

    class Config:
        env_file = ".env"


# Single shared instance - import this everywhere when we need config.
# Never call os.getenv() directly in our code , always use settings.FIELD_NAME.

settings = Settings()