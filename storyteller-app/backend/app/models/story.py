import sqlalchemy as sa
from sqlalchemy.dialects.sqlite import JSON # For SQLite specific JSON type
from sqlalchemy.orm import relationship
import datetime

from .base import Base

class Story(Base):
    __tablename__ = "stories"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    title = sa.Column(sa.String, index=True, nullable=False)
    content_raw = sa.Column(sa.Text, nullable=False) # Full story text from Gemini

    # Formatted pages: Store as JSON. Each page could be an object with text and image_placeholder_id
    # Example: [{"page_num": 1, "text": "...", "layout": "image_right", "image_id": "img_placeholder_1"}, ...]
    formatted_pages = sa.Column(JSON, nullable=True) # Using generic JSON for broader compatibility

    # Main character relationship
    main_character_id = sa.Column(sa.Integer, sa.ForeignKey("characters.id"), nullable=False)
    main_character = relationship("Character", back_populates="stories_as_main")

    # Supporting characters - can be a JSON list of names or IDs for simplicity
    # Or, a many-to-many relationship if characters are predefined and selectable.
    # For now, let's assume a list of names/descriptions.
    supporting_characters_info = sa.Column(JSON, nullable=True) # e.g. ["Lion the Brave", "Timmy the Turtle"]

    # Metadata
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    is_favorite = sa.Column(sa.Boolean, default=False, nullable=False)
    moral_lessons = sa.Column(JSON, nullable=True) # e.g. ["Be kind", "Work together"]
    theme = sa.Column(sa.String, nullable=True) # e.g., "Adventure", "Friendship"

    # Relationship to StoryImages (one story can have many images)
    images = relationship("StoryImage", back_populates="story", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Story(id={self.id}, title='{self.title}')>"
