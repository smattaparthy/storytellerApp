from pydantic import BaseModel, Field
from typing import Optional, List

# Base properties shared by all character schemas
class CharacterBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Name of the character")
    personality_traits: Optional[str] = Field(None, max_length=255, description="Comma-separated personality traits")
    emoji: Optional[str] = Field(None, max_length=10, description="A single emoji representing the character")
    description: Optional[str] = Field(None, max_length=1000, description="A brief description of the character")

# Schema for creating a new character (e.g., via an admin endpoint)
class CharacterCreate(CharacterBase):
    pass

# Schema for updating an existing character
class CharacterUpdate(CharacterBase):
    name: Optional[str] = Field(None, min_length=2, max_length=100) # All fields optional for update
    # Other fields from CharacterBase are implicitly optional via Pydantic's update model behavior if not redefined

# Properties shared by models stored in DB
class CharacterInDBBase(CharacterBase):
    id: int

    class Config:
        from_attributes = True # Pydantic V2 way to enable ORM mode

# Schema for returning a character from the API (what the user sees)
class Character(CharacterInDBBase):
    pass # Inherits all fields from CharacterInDBBase

# Schema for a list of characters (e.g., for GET /characters)
class CharacterList(BaseModel):
    characters: List[Character]
    count: int

# If you plan to have predefined characters in the DB that are not user-creatable through the main API,
# CharacterCreate and CharacterUpdate might only be used for admin purposes or initial seeding.
# The main API would primarily use the Character schema for responses.
