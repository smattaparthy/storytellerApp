# FastAPI application entry point
from fastapi import FastAPI

# Rename the FastAPI instance to avoid conflict with the 'app' package name
fastapi_application = FastAPI(title="Storyteller API", version="0.1.0")

@fastapi_application.get("/")
async def read_root():
    return {"message": "Welcome to the Storyteller API"}

# Further imports and router configurations will be added here
# e.g., from .api import stories_router, characters_router
# from .core.database import engine, Base
# from .models import story, character # Import models to ensure they are registered with SQLAlchemy

from app.core.database import create_db_and_tables, close_db_connection
# Ensure all models are imported so Base.metadata knows about them
# This can be done by importing the models module or individual models
import app.models # This will trigger models/__init__.py

@fastapi_application.on_event("startup")
async def startup_event():
    """
    Actions to perform on application startup.
    - Creates database tables if they don't exist.
    """
    print("Application startup: Creating database tables...")
    await create_db_and_tables()
    print("Application startup: Database tables checked/created.")

@fastapi_application.on_event("shutdown")
async def shutdown_event():
    """
    Actions to perform on application shutdown.
    - Closes database connections.
    """
    print("Application shutdown: Closing database connection...")
    await close_db_connection()
    print("Application shutdown: Database connection closed.")

# API Routers
from app.api import stories as stories_router
from app.api import characters as characters_router

# Include routers from the api module
# Using a common prefix for all API endpoints, e.g., /api
# Versioning can be done like /api/v1/ if needed
fastapi_application.include_router(characters_router.router, prefix="/api", tags=["Characters"])
fastapi_application.include_router(stories_router.router, prefix="/api", tags=["Stories"])

if __name__ == "__main__":
    import uvicorn
    # This is for direct execution, e.g. `python app/main.py`
    # Uvicorn will typically be run from the command line as per project instructions
    uvicorn.run(fastapi_application, host="0.0.0.0", port=8000)
