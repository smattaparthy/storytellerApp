from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db_session
# from app.models.character import Character as CharacterModel # SQLAlchemy model
# from app.schemas.character import Character, CharacterCreate # Pydantic schemas (to be created)

from sqlalchemy import select # For database queries

from app.models.character import Character as CharacterModel # SQLAlchemy model
from app.schemas.character import Character as CharacterSchema, CharacterCreate, CharacterList # Pydantic schemas

router = APIRouter()

# In a real app, characters might be pre-populated or managed via an admin interface.
# For now, we'll keep the dummy data, but it should ideally query the DB.
# Let's assume there's a way to populate these, e.g., on startup or via another script.

async def _get_or_create_dummy_characters(db: AsyncSession) -> List[CharacterModel]:
    """Helper to ensure dummy characters exist for basic API functionality."""
    dummy_char_data = [
        {"name": "Ellie the Elephant", "personality_traits": "Wise, Gentle", "emoji": "🐘", "description": "A kind elephant who loves to explore."},
        {"name": "Leo the Lion", "personality_traits": "Brave, Playful", "emoji": "🦁", "description": "A courageous lion with a magnificent mane."},
        {"name": "Tilly the Tiger", "personality_traits": "Curious, Energetic", "emoji": "🐅", "description": "A striped tiger always ready for an adventure."},
        {"name": "Rory the Rabbit", "personality_traits": "Quick, Clever", "emoji": "🐇", "description": "A fluffy rabbit known for its speed and smarts."},
        {"name": "Penny the Penguin", "personality_traits": "Friendly, Funny", "emoji": "🐧", "description": "A charming penguin who loves to tell jokes."},
    ]

    characters = []
    for char_data in dummy_char_data:
        result = await db.execute(select(CharacterModel).filter_by(name=char_data["name"]))
        character = result.scalars().first()
        if not character:
            character = CharacterModel(**char_data)
            db.add(character)
            await db.flush() # Flush to get ID if needed immediately, or commit later
        characters.append(character)
    # A single commit after adding all missing characters is more efficient
    # For this helper, we might not commit here, let the endpoint handle it or rely on get_db_session commit.
    # However, for this specific use case of ensuring they exist for a GET, committing makes sense.
    await db.commit()
    for char in characters: # Refresh to get committed state if IDs were generated
        await db.refresh(char)
    return characters


@router.get("/characters", response_model=List[CharacterSchema]) # Using new Character schema
async def get_all_characters(
    db: AsyncSession = Depends(get_db_session)
):
    """
    Retrieve all available predefined characters.
    """
    # For now, ensure dummy characters are in DB and return them.
    # In a production system, these would be managed properly.
    # This is a temporary measure to make the endpoint functional with the DB.
    await _get_or_create_dummy_characters(db) # Ensure they exist

    result = await db.execute(select(CharacterModel).order_by(CharacterModel.id))
    characters = result.scalars().all()

    # Convert SQLAlchemy models to Pydantic schemas before returning
    # Pydantic's from_orm or from_attributes will handle this if response_model is set.
    return characters


# Example of a POST endpoint if characters were user-creatable:
# @router.post("/characters", response_model=CharacterSchema, status_code=201)
# async def create_new_character(
#     character: CharacterCreate, # Pydantic schema for creation
#     db: AsyncSession = Depends(get_db_session)
# ):
#     # db_character = CharacterModel(**character.dict())
#     # db.add(db_character)
#     # await db.commit()
#     # await db.refresh(db_character)
#     # return db_character
#     pass

# @router.get("/characters/{character_id}", response_model=CharacterSchema)
# async def get_character_by_id(
#     character_id: int,
#     db: AsyncSession = Depends(get_db_session)
# ):
#     # character = await db.get(CharacterModel, character_id)
#     # if not character:
#     #     raise HTTPException(status_code=404, detail="Character not found")
#     # return character
#     pass
