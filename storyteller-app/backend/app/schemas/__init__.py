# Makes 'schemas' a Python package
# This file can also be used to conveniently import all schemas

from .character import Character, CharacterCreate, CharacterUpdate, CharacterInDBBase
# StoryCreate was effectively replaced by StoryCreateRequest for API input and StoryCreateInternal for internal model prep.
# Exporting StoryCreateRequest as it's used by API layers.
from .story import Story, StoryCreateRequest, StoryUpdate, StoryInDBBase, StoryPage, StoryGenerated
from .story_image import StoryImage, StoryImageCreate, StoryImageUpdate, StoryImageInDBBase
from .common import PaginatedResponse # For paginated list responses, if needed

__all__ = [
    "Character",
    "CharacterCreate", # This is defined in character.py
    "CharacterUpdate",
    "CharacterInDBBase",
    "Story",
    "StoryCreateRequest", # Changed from StoryCreate
    "StoryUpdate",
    "StoryInDBBase",
    "StoryPage",
    "StoryGenerated",
    "StoryImage",
    "StoryImageCreate", # This is defined in story_image.py
    "StoryImageUpdate",
    "StoryImageInDBBase",
    "PaginatedResponse",
]
