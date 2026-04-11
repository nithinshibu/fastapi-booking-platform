from fastapi import FastAPI
from sqlalchemy import text
from app.db.session import engine

# Think of this as the Program.cs - it creates the app and wires everything together.
# As we add features , we will import and register more routes here.

app = FastAPI(
    title="Booking Platform API",
    description = "Movie and Event Booking Platform - Learning Project",
    version = "1.0.0"
)

@app.on_event("startup")
def verify_database_connection():
    """ 
    Runs once when the server starts - equivalent to calling the Database.CanConnect()
    in .NET on application startup. Fails if the DB is unreachable so we
    catch config errors immediately instead of on the first real request. 
    """
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))


@app.get("/health",tags=["Health"])
def health_check():
    """
    Simple health check endpoint.
    Returns 200 OK if the server is running. 
    """
    return {"status":"ok"}