from fastapi import FastAPI

# Think of this as the Program.cs - it creates the app and wires everything together.
# As we add features , we will import and register more routes here.

app = FastAPI(
    title="Booking Platform API",
    description = "Movie and Event Booking Platform - Learning Project",
    version = "1.0.0"
)

@app.get("/health",tags=["Health"])
def health_check():
    """
    Simple health check endpoint.
    Returns 200 OK if the server is running. 
    """
    return {"status":"ok"}