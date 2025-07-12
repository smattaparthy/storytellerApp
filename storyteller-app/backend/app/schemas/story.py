from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
import datetime

from .character import Character # For embedding character details
from .story_image import StoryImage, StoryImageMinimal # For embedding image details

# Represents a single formatted page of a story
class StoryPage(BaseModel):
    page_num: int = Field(..., description="The sequential page number")
    text: str = Field(..., description="Text content of the page")
    layout: str = Field(default="text_only", description="Layout type: e.g., 'text_only', 'image_right', 'image_left', 'full_page_image'")
    image_id: Optional[int] = Field(None, description="ID of the StoryImage record associated with this page")
    # image_data_base64: Optional[str] = Field(None, description="Base64 image data (if embedded directly on page object)")
    image: Optional[StoryImageMinimal] = Field(None, description="Minimal image details for this page")


# Base properties for a story
class StoryBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=150, description="Title of the story")
    theme: Optional[str] = Field(None, max_length=100, description="Main theme or topic of the story")
    main_character_id: int = Field(..., description="ID of the main character for the story")
    # supporting_character_ids: Optional[List[int]] = Field(default_factory=list, description="List of IDs for supporting characters")
    supporting_characters_info: Optional[List[Dict[str, Any]]] = Field(default_factory=list, description="Information about supporting characters, e.g., [{'id': 1, 'name': 'Leo'}] or freeform text if not linked to Character model directly.")


# Schema for creating a new story (data received by the /generate endpoint)
class StoryCreateRequest(BaseModel): # Renamed from StoryCreate to be more specific to request
    main_character_id: int = Field(..., description="ID of the main character")
    supporting_character_ids: Optional[List[int]] = Field(default_factory=list, description="List of IDs for supporting characters")
    story_theme: str = Field(default="Adventure", max_length=100, description="Theme for the story")
    # Any other parameters for story generation can be added here

# This schema would be used internally after generation, before saving to DB
class StoryCreateInternal(StoryBase):
    content_raw: str # Full text from AI
    formatted_pages: Optional[List[StoryPage]] = Field(default_factory=list)
    moral_lessons: Optional[List[str]] = Field(default_factory=list)
    # images will be StoryImageCreate objects, handled separately or as part of a service layer
    # This schema represents the Story model's fields before it's an InDBBase model.

# Schema for updating an existing story (e.g., marking as favorite, changing title)
class StoryUpdate(BaseModel): # Not inheriting StoryBase to allow partial updates
    title: Optional[str] = Field(None, min_length=3, max_length=150)
    is_favorite: Optional[bool] = None
    # Other fields that might be updatable

# Properties shared by models stored in DB
class StoryInDBBase(StoryBase):
    id: int
    content_raw: str # The full, unpaginated story text from Gemini
    formatted_pages: Optional[List[StoryPage]] = Field(default_factory=list) # Stored as JSON in DB
    moral_lessons: Optional[List[str]] = Field(default_factory=list) # Stored as JSON in DB
    created_at: datetime.datetime
    is_favorite: bool = False

    # Relationships (if you want to fetch them and include in response)
    # main_character: Optional[Character] = None # This would be populated by service layer
    # images: List[StoryImage] = [] # This would be populated by service layer

    class Config:
        from_attributes = True

# Schema for returning a full story from the API (what the user sees)
class Story(StoryInDBBase):
    # If you want to include related objects in the response:
    main_character: Optional[Character] = None # Populated after fetching from DB
    images: List[StoryImageMinimal] = [] # List of minimal image info, not full base64 unless needed

# Schema for the response from the /generate endpoint
class StoryGenerated(Story): # Or a more specific schema
    # Could include additional fields specific to generation result, e.g., generation_time_ms
    pass

# Schema for a list of stories (e.g., for GET /stories or /stories/favorites)
class StoryList(BaseModel):
    stories: List[Story] # Could be StoryInDBBase or a more minimal StorySummary schema
    count: int

# Schema for returning just the formatted pages of a story for reading view
class StoryPagesResponse(BaseModel):
    story_id: int
    title: str
    pages: List[StoryPage]
