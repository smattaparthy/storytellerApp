import sqlalchemy as sa
from sqlalchemy.orm import relationship
from .base import Base

class Character(Base):
    __tablename__ = "characters"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, unique=True, index=True, nullable=False)
    # Personality traits could be a JSON field or a separate table if more complex
    personality_traits = sa.Column(sa.String) # Simple string for now, e.g., "Brave, Curious"
    emoji = sa.Column(sa.String, nullable=True)
    description = sa.Column(sa.Text, nullable=True) # A brief description of the character

    # Relationship to stories (e.g., if a character is a "main_character" in a story)
    # This is a one-to-many relationship from Character to Story (one character can be the main in many stories)
    stories_as_main = relationship("Story", back_populates="main_character")

    # If supporting characters are linked via an association table, that would be defined here.
    # For now, we assume supporting characters are stored differently, perhaps as a list of names or IDs in the Story model.

    def __repr__(self):
        return f"<Character(id={self.id}, name='{self.name}')>"
