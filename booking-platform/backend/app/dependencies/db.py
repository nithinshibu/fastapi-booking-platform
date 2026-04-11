from collections.abc import Generator
from sqlalchemy.orm import Session
from app.db.session import SessionLocal

def get_db() -> Generator[Session,None,None]:
    """
    FastAPI dependency that provides a database session for a single request.

    This is the equivalent of a scoped DbContext in .NET:
    - A new session is created at the start of each request.
    - It's automatically closed when the request finishes (even if an error occurs)

    Usage in a route (just like injecting IAppDbContext via constructor):
        def my_route(db:Session = Depends(get_db)):
            pass

    """

    db = SessionLocal()
    try:
        yield db   # <-- the route handler runs here , with the db injected
    finally:
        db.close()   # <-- always runs after the request, success or error