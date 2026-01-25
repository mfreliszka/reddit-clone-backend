import pytest
import pytest_asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture(scope="function")
def test_app():
    return app

@pytest_asyncio.fixture(scope="function")
async def client(test_app):
    async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as c:
        yield c

@pytest.fixture
def unique_username() -> str:
    return f"user_{uuid.uuid4().hex[:8]}"

@pytest.fixture
def unique_email(unique_username) -> str:
    return f"{unique_username}@example.com"
