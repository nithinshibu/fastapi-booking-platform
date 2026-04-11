from fastapi import FastAPI
from sqlalchemy import text

from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.users import router as users_router
from app.db.session import engine

# Think of this as the Program.cs - it creates the app and wires everything together.
# Each router is registered here with include_router, equivalent to 
# app.MapControllers() / builders.Services.AddControllers() in .NET
# As we add features (movies,shows,bookings), we will import and register
# their routers here in the same way.

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

# Register routers - prefix="/api/v1" is added here , not in the router itself,
# so the router stays reusable if we ever need to mount it at a different version.
app.include_router(auth_router,prefix="/api/v1")
app.include_router(users_router,prefix="/api/v1")


@app.get("/health",tags=["Health"])
def health_check():
    """
    Simple health check endpoint.
    Returns 200 OK if the server is running. 
    """
    return {"status":"ok"}