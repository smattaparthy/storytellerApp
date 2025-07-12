from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any, Dict

from app.core.database import get_db_session
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload


from app.models.character import Character as CharacterModel
from app.models.story import Story as StoryModel
from app.models.story_image import StoryImage as StoryImageModel
from app.schemas.story import (
    Story as StorySchema,
    StoryCreateRequest,
    StoryGenerated, # Using this for the generate response
    StoryPage as StoryPageSchema, # Renamed for clarity
    StoryList,
    StoryUpdate as StoryUpdateSchema # Schema for updating story (e.g. favorite)
)
from app.schemas.common import MessageResponse # For simple messages
from app.services.story_generator import GeminiStoryService
from app.services.image_generator import ImagenService
from app.services.page_formatter import PageFormatter
from app.core.config import settings # For MAX_IMAGES_PER_STORY

router = APIRouter()

# --- Dependency Injection for Services ---
# These can be overridden in tests with mock services if needed.
def get_story_generator_service():
    return GeminiStoryService()

def get_image_generator_service():
    return ImagenService()

def get_page_formatter_service():
    return PageFormatter(max_images_per_story=settings.MAX_IMAGES_PER_STORY)
# --- End Dependency Injection ---


@router.post("/stories/generate", response_model=StoryGenerated, status_code=201)
async def generate_new_story(
    request_data: StoryCreateRequest,
    db: AsyncSession = Depends(get_db_session),
    story_service: GeminiStoryService = Depends(get_story_generator_service),
    image_service: ImagenService = Depends(get_image_generator_service),
    page_formatter: PageFormatter = Depends(get_page_formatter_service)
):
    """
    Generate a new story with images and formatted pages, then save it to the database.
    """
    # 1. Fetch character details from DB
    main_char_result = await db.get(CharacterModel, request_data.main_character_id)
    if not main_char_result:
        raise HTTPException(status_code=404, detail=f"Main character with id {request_data.main_character_id} not found.")

    supporting_chars_names = []
    if request_data.supporting_character_ids:
        for char_id in request_data.supporting_character_ids:
            sup_char = await db.get(CharacterModel, char_id)
            if sup_char:
                supporting_chars_names.append(sup_char.name)
            else:
                print(f"Warning: Supporting character with id {char_id} not found. Skipping.")

    # 2. Generate story content and image prompts using StoryService
    try:
        generated_content = await story_service.generate_story_and_prompts(
            main_character_name=main_char_result.name,
            supporting_character_names=supporting_chars_names,
            theme=request_data.story_theme,
            story_length_words=settings.MAX_STORY_LENGTH # Example, could be configurable
        )
    except Exception as e:
        # Log the exception e
        raise HTTPException(status_code=500, detail=f"Story generation failed: {str(e)}")

    # 3. Generate images using ImageService
    generated_images_base64 = []
    if generated_content.get("image_prompts"):
        try:
            generated_images_base64 = await image_service.generate_images_base64(generated_content["image_prompts"])
        except Exception as e:
            # Log the exception e
            # Decide if to proceed without images or fail
            print(f"Warning: Image generation failed: {str(e)}. Proceeding without images or with fewer images.")
            # Fallback: ensure generated_images_base64 is a list of Nones or empty
            generated_images_base64 = [None] * len(generated_content["image_prompts"])


    # 4. Create StoryImage objects (without saving to DB yet, just preparing them)
    # These will be linked to the StoryModel later via relationship.
    story_image_objects_to_save = []
    for i, prompt in enumerate(generated_content.get("image_prompts", [])):
        if i < len(generated_images_base64) and generated_images_base64[i]:
            # The placeholder_id links the prompt/image to a specific part of the story content stubs
            # The GeminiStoryService mock provides "image_placeholder_id" in its paginated_content_stubs
            # We need to match this.
            # Find the stub that this image prompt corresponds to (e.g., by index or a more robust ID)
            # For mock, assume prompts[i] links to paginated_content_stubs[i]'s image_placeholder_id
            placeholder_id_for_image = generated_content["paginated_content_stubs"][i].get("image_placeholder_id") if i < len(generated_content["paginated_content_stubs"]) else f"img_prompt_idx_{i}"

            story_image_objects_to_save.append(
                StoryImageModel(
                    image_prompt=prompt,
                    image_data_base64=generated_images_base64[i],
                    image_placeholder_id=placeholder_id_for_image
                    # story_id will be set by SQLAlchemy relationship
                )
            )

    # 5. Format story into pages using PageFormatter
    # The PageFormatter needs the image objects (or dicts representing them) to embed data.
    # Let's convert StoryImageModel instances (not yet saved) to dicts for the formatter for now.
    # This is a bit clunky; a real PageFormatter might take image prompts and base64 data directly.
    # Or, it could take StoryImageModel instances if they have temporary IDs.
    # For the mock, let's prepare dicts similar to what the formatter expects.

    # The current mock PageFormatter expects dicts like:
    # {"id": "temp_id", "image_placeholder_id": "...", "image_data_base64": "..."}
    # We'll use the prompt as a temporary ID or index for linking.
    image_data_for_formatter = []
    for i, img_model in enumerate(story_image_objects_to_save):
        image_data_for_formatter.append({
            "id": f"temp_img_{i}", # Temporary ID for formatter context
            "image_placeholder_id": img_model.image_placeholder_id,
            "image_data_base64": img_model.image_data_base64,
            "image_prompt": img_model.image_prompt
        })

    formatted_pages_data = await page_formatter.format_story_into_pages(
        story_title=generated_content["title"],
        raw_story_content=generated_content["full_content_raw"], # For reference, stubs are primary
        paginated_content_stubs=generated_content["paginated_content_stubs"],
        story_images=image_data_for_formatter
    )

    # 6. Save Story and linked StoryImages to DB
    db_story = StoryModel(
        title=generated_content["title"],
        content_raw=generated_content["full_content_raw"],
        formatted_pages=formatted_pages_data, # This is JSON
        main_character_id=request_data.main_character_id,
        supporting_characters_info=[{"name": name} for name in supporting_chars_names], # Example structure
        moral_lessons=generated_content.get("moral_lessons", []),
        theme=generated_content.get("theme_echo", request_data.story_theme),
        images=story_image_objects_to_save # Link the StoryImageModel instances
    )

    db.add(db_story)
    await db.commit()
    await db.refresh(db_story, attribute_names=['id', 'created_at']) # Refresh to get ID and default values
    # Refresh related images to get their generated IDs too
    # This requires loading the relationship.
    await db.refresh(db_story, attribute_names=['images'])
    for img in db_story.images: # Ensure image IDs are loaded
        await db.refresh(img)


    # 7. Prepare and return the response using StoryGenerated schema
    # This requires StoryGenerated to be able to serialize the main_character and images relationships.
    # We need to load them explicitly for the response model if they are part of it.

    # Re-fetch the story with relationships for the response model
    # (or ensure db_story has them correctly populated after refresh)
    # For Pydantic's from_attributes to work with relationships, they need to be loaded.
    # The `await db.refresh(db_story, attribute_names=['images'])` loads the images.
    # For main_character, it's not loaded by default with refresh.

    # Let's construct the response schema manually or ensure data is loaded for from_attributes.
    # The StoryGenerated schema (which inherits from Story) expects main_character: Optional[Character]
    # and images: List[StoryImageMinimal].

    # Populate main_character for the response
    db_story.main_character = main_char_result # We already have this model

    # The images on db_story are StoryImageModel. StoryGenerated expects StoryImageMinimal.
    # Pydantic should handle this conversion if StoryImageMinimal.Config.from_attributes = True.

    return db_story # FastAPI will convert this using StoryGenerated response_model


@router.get("/stories", response_model=StoryList)
async def get_all_stories(
    db: AsyncSession = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve all stories, with optional pagination.
    Loads main character and image information for each story.
    """
    result = await db.execute(
        select(StoryModel)
        .options(
            selectinload(StoryModel.main_character), # Eager load main character
            selectinload(StoryModel.images)          # Eager load images
        )
        .order_by(StoryModel.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    stories = result.scalars().all()

    # For a proper paginated response, we'd also need a total count.
    # total_count_result = await db.execute(select(func.count(StoryModel.id)))
    # total_count = total_count_result.scalar_one()

    return StoryList(stories=stories, count=len(stories)) # Simplified count for now


@router.get("/stories/favorites", response_model=StoryList)
async def get_favorite_stories(
    db: AsyncSession = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100
):
    """
    Get favorite stories only, with optional pagination.
    """
    result = await db.execute(
        select(StoryModel)
        .where(StoryModel.is_favorite == True)
        .options(
            selectinload(StoryModel.main_character),
            selectinload(StoryModel.images)
        )
        .order_by(StoryModel.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    stories = result.scalars().all()
    return StoryList(stories=stories, count=len(stories)) # Simplified count


@router.get("/stories/{story_id}/pages", response_model=List[StoryPageSchema])
async def get_story_pages_for_reading( # Renamed from get_story_pages to avoid conflict with schema name
    story_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get formatted story pages for a specific story for the reading view.
    """
    story = await db.get(StoryModel, story_id)
    if not story:
        raise HTTPException(status_code=404, detail=f"Story with id {story_id} not found.")

    if not story.formatted_pages:
        # This case should ideally not happen if pages are generated and saved with the story.
        # If it can happen, we might need to call PageFormatter here on raw_content.
        # For now, assume formatted_pages is always populated.
        raise HTTPException(status_code=404, detail=f"Story with id {story_id} has no formatted pages.")

    # The formatted_pages in DB is a list of dicts.
    # We need to convert them to List[StoryPageSchema].
    # Pydantic should do this automatically if the structure matches.
    return story.formatted_pages


@router.patch("/stories/{story_id}/favorite", response_model=StorySchema)
async def toggle_story_favorite_status(
    story_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Toggle the favorite status of a story.
    """
    story = await db.get(StoryModel, story_id)
    if not story:
        raise HTTPException(status_code=404, detail=f"Story with id {story_id} not found.")

    story.is_favorite = not story.is_favorite
    await db.commit()
    await db.refresh(story)
    # To include main_character and images in response, load them:
    await db.refresh(story, attribute_names=['main_character', 'images'])
    return story


@router.delete("/stories/{story_id}", response_model=MessageResponse)
async def delete_story_by_id(
    story_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Delete a story by its ID.
    """
    story = await db.get(StoryModel, story_id)
    if not story:
        raise HTTPException(status_code=404, detail=f"Story with id {story_id} not found.")

    await db.delete(story)
    await db.commit()
    return MessageResponse(message=f"Story with id {story_id} deleted successfully.")
