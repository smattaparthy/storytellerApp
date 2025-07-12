import sys
import os
# Add the 'backend' directory to sys.path to ensure 'app' is found correctly.
# This assumes conftest.py is in backend/tests/
# So, os.path.dirname(__file__) is backend/tests/
# os.path.join(os.path.dirname(__file__), '..') is backend/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport # Import ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator, Generator

# Alias the import of the FastAPI app instance
from app.main import fastapi_application as main_fastapi_app # Updated to use the new name
from app.core.config import Settings, settings as app_settings
from app.models.base import Base
from app.core.database import get_db_session

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_storyteller.db"

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def test_settings() -> Settings:
    current_env_vars = app_settings.model_dump()
    current_env_vars["DATABASE_URL"] = TEST_DATABASE_URL
    if not current_env_vars.get("GOOGLE_API_KEY"):
        current_env_vars["GOOGLE_API_KEY"] = "mock_api_key_for_testing"
    return Settings(**current_env_vars)

@pytest_asyncio.fixture(scope="session")
async def test_engine(test_settings: Settings):
    engine = create_async_engine(test_settings.DATABASE_URL, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()
    if os.path.exists("./test_storyteller.db"):
        os.remove("./test_storyteller.db")

@pytest_asyncio.fixture(scope="function")
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    connection = await test_engine.connect()
    transaction = await connection.begin()
    TestScopedSessionFactory = sessionmaker(
        bind=connection,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
    async with TestScopedSessionFactory() as session:
        yield session
    if transaction.is_active:
        await transaction.rollback()
    await connection.close()

@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession, test_settings: Settings) -> AsyncGenerator[AsyncClient, None]:
    def override_get_db_session() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    # Use the aliased FastAPI app instance
    main_fastapi_app.dependency_overrides[get_db_session] = override_get_db_session

    transport = ASGITransport(app=main_fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac

    del main_fastapi_app.dependency_overrides[get_db_session]

# Ensure models are loaded for Base.metadata
import app.models
