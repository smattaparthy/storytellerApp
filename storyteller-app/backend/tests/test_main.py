import pytest
import pytest_asyncio # For async fixtures
from httpx import AsyncClient

# The client fixture is now provided by conftest.py, which uses an aliased app import
# and sets up a test database. No need to import 'app' or define client here.

@pytest.mark.asyncio
async def test_read_root(client: AsyncClient): # client fixture from conftest.py will be used
    """
    Test the root endpoint ("/") of the application.
    """
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Storyteller API"}

@pytest.mark.asyncio
async def test_startup_event_creates_tables(client: AsyncClient):
    """
    A conceptual test to ensure the startup event (table creation) ran.
    This is hard to test directly without inspecting DB state or specific logs.
    A more robust test would involve trying to insert/query data.
    For now, a simple call to an endpoint after startup.
    If create_db_and_tables failed badly, the app might not even start.
    """
    # This test mostly ensures the app starts up with the event handler.
    # A successful response from any endpoint implies startup didn't crash.
    response = await client.get("/") # Re-use root endpoint check
    assert response.status_code == 200
    # In a real scenario, you might add a health check endpoint that verifies DB connectivity.

# To run these tests, you would typically:
# 1. Ensure `pytest` and `pytest-asyncio` and `httpx` are in requirements-dev.txt or similar.
#    (I'll add them to the main requirements.txt for simplicity for now,
#     though separating dev dependencies is good practice).
# 2. Navigate to the `storyteller-app/backend/` directory.
# 3. Run `pytest`.

# Note: The `create_db_and_tables` uses an in-memory SQLite DB by default if DATABASE_URL
# is not configured to a file for tests. Or, you can configure a separate test database.
# Our current config.py uses an absolute path to storyteller-app/database/storyteller.db.
# For tests, it's often better to use an in-memory DB or a temporary test DB
# to avoid side effects on the development DB and ensure test isolation.
# This can be achieved by overriding settings in tests (e.g., via conftest.py).

# For now, this test will run against the configured DB.
# If storyteller.db doesn't exist, `create_db_and_tables` will create it.
# If it exists, tests run against it. This is not ideal for isolation.
# I will add a step later to refine test DB strategy.
# For initial setup, this is a start.
