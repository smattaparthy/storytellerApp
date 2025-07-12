from pydantic import BaseModel, Field
from typing import Optional

# Base properties for a story image
class StoryImageBase(BaseModel):
    image_prompt: str = Field(..., description="The prompt used to generate this image")
    page_number: Optional[int] = Field(None, description="Page number this image is primarily associated with")
    image_placeholder_id: Optional[str] = Field(None, index=True, description="A temporary ID used by PageFormatter to link text to an image stub before full StoryImage record exists")

# Schema for creating a new story image (internal use primarily, as images are part of story generation)
# This might include the base64 data directly if creating from an existing image.
class StoryImageCreate(StoryImageBase):
    image_data_base64: str = Field(..., description="Base64 encoded image data")
    story_id: int # Required when creating and linking to a story

# Schema for updating a story image (e.g., changing prompt or page number)
class StoryImageUpdate(StoryImageBase):
    image_prompt: Optional[str] = None
    # image_data_base64: Optional[str] = None # Usually not updated, but regenerated
    # page_number: Optional[int] = None # Already in base

# Properties shared by models stored in DB
class StoryImageInDBBase(StoryImageBase):
    id: int
    story_id: int
    image_data_base64: str # In DB, this is not optional

    class Config:
        from_attributes = True

# Schema for returning a story image from the API
class StoryImage(StoryImageInDBBase):
    pass # Inherits fields

# If you only return image URLs or IDs instead of full base64 in some contexts:
class StoryImageMinimal(BaseModel):
    id: int
    page_number: Optional[int]
    image_url: Optional[str] = None # If you generate URLs instead of embedding base64
    image_placeholder_id: Optional[str] = None

    class Config:
        from_attributes = True
