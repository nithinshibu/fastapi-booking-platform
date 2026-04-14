from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.movies import router as movies_router
from app.api.v1.routes.shows import router as shows_router
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

# CORS (Cross Origin Resource Sharing) - MUST be added before any routes 

""" 

Without this, the browser refuses to send requests from http://localhost:5173 (our React app)
to http://localhost:8000 (FastAPI) because they are on different ports, 
which counts as a different origin.

# allow_origins: which domains can call this API (Vite dev server uses port 5173)
# allow_credentials: needed if you ever send cookies (good to have on)
# allow_methods: which HTTP methods are permitted
# allow_headers: which request headers are allowed (Authorization is required for JWT)

"""

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers = ["*"]
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
app.include_router(movies_router,prefix="/api/v1")
app.include_router(shows_router,prefix="/api/v1")



@app.get("/health",tags=["Health"])
def health_check():
    """
    Simple health check endpoint.
    Returns 200 OK if the server is running. 
    """
    return {"status":"ok"}