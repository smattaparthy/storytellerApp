from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

from .config import settings # Import the global settings instance
from app.models.base import Base # Import Base for metadata

# Create an async SQLAlchemy engine
# The DATABASE_URL is taken from the settings object, which resolves paths correctly.
engine = create_async_engine(
    settings.DATABASE_URL,
    # echo=True, # Enable SQL logging for debugging (optional)
    future=True # Use the future pool for async operations
)

# Create an async session factory
# expire_on_commit=False is often useful with FastAPI dependencies
# to allow objects to be accessed after the session is closed.
AsyncSessionFactory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False, # Typically False for async sessions managed per request
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get an async database session.
    Ensures the session is closed after the request.
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit() # Commit changes if no exceptions occurred
        except Exception:
            await session.rollback() # Rollback on error
            raise
        finally:
            await session.close() # Ensure session is closed

async def create_db_and_tables():
    """
    Creates all database tables defined in SQLAlchemy models.
    This is typically called once on application startup.
    For production, Alembic migrations are preferred.
    """
    async with engine.begin() as conn:
        # In an async context, run_sync is used for DDL operations
        # await conn.run_sync(Base.metadata.drop_all) # Optional: drop all tables for a fresh start
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created (if they didn't exist).")

async def close_db_connection():
    """
    Closes the database engine connection.
    Typically called on application shutdown.
    """
    await engine.dispose()
    print("Database connection closed.")

# Note: Base.metadata needs to have all models imported somewhere before create_all is called.
# This is usually handled by importing model modules in main.py or models/__init__.py.
# Our models/__init__.py imports all models, and Base is also imported there.
# We also import Base here, ensuring its metadata is populated.
# Ensure models are imported so Base.metadata knows about them:
# from app.models import story, character, story_image # Not strictly needed here if models/__init__ does it.
# The import of Base from app.models.base should be sufficient if models are linked to that Base.
