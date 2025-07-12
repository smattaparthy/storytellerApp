import sqlalchemy as sa
from sqlalchemy.orm import relationship
from .base import Base

class StoryImage(Base):
    __tablename__ = "story_images"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    story_id = sa.Column(sa.Integer, sa.ForeignKey("stories.id"), nullable=False)

    # Image data - Base64 encoded string. For large amounts, consider storing paths to files.
    # SQLite has limits on blob/text sizes, but for a few images per story, this might be acceptable.
    image_data_base64 = sa.Column(sa.Text, nullable=False)

    # Prompt used to generate the image
    image_prompt = sa.Column(sa.Text, nullable=False)

    # Page number this image is associated with in the story
    page_number = sa.Column(sa.Integer, nullable=True) # Can be null if it's a general story image

    # A placeholder or identifier used by PageFormatter before actual image_id is known
    # This helps link text content to where an image should be.
    image_placeholder_id = sa.Column(sa.String, nullable=True, index=True)

    # Relationship back to the Story
    story = relationship("Story", back_populates="images")

    def __repr__(self):
        return f"<StoryImage(id={self.id}, story_id={self.story_id}, page_number={self.page_number})>"
