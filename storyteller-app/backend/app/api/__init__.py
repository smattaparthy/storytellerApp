# This file makes the 'api' directory a Python package.
# You can also define a collective API router here if you want to group all API versions or modules.

# Example:
# from fastapi import APIRouter
# from . import stories, characters # Assuming your files are stories.py, characters.py

# api_router_v1 = APIRouter(prefix="/v1")
# api_router_v1.include_router(stories.router, tags=["Stories Endpoints"])
# api_router_v1.include_router(characters.router, tags=["Characters Endpoints"])

# This allows main.py to do:
# from app.api import api_router_v1
# app.include_router(api_router_v1)

# For now, we'll keep it simple and let main.py import individual routers.
# This file can remain empty or be used for future structuring.

# To make it easy to import routers directly:
from . import stories
from . import characters

__all__ = ["stories", "characters"]
