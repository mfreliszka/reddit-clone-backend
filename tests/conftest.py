import pytest
import pytest_asyncio
import uuid
from unittest.mock import MagicMock, AsyncMock
from httpx import AsyncClient, ASGITransport
from litestar import Litestar
from app.main import app


from typing import Iterator

@pytest.fixture(scope="function")
def test_app() -> Iterator[Litestar]:
    """
    Fixture to provide the Litestar app instance.
    """
    yield app


@pytest_asyncio.fixture(scope="function")
async def client(test_app: Litestar):
    """
    Fixture to provide an AsyncClient for the Litestar app.
    """
    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://test"
    ) as c:
        yield c


@pytest.fixture
def unique_username() -> str:
    return f"user_{uuid.uuid4().hex[:8]}"


@pytest.fixture
def unique_email(unique_username) -> str:
    return f"{unique_username}@example.com"

@pytest.fixture
def mock_auth(mocker):
    """
    Fixture to mock authentication middleware dependencies.
    Bypasses DB lookup and Token decoding.
    Returns:
        MagicMock: The mocked User ORM object to allow customization if needed.
    """
    # Mock User ORM in middleware
    mock_user_orm = MagicMock()
    mock_query = AsyncMock()
    # Default user found
    mock_query.first.return_value = {
        "id": 1, 
        "username": "testuser", 
        "email": "test@example.com", 
        "is_active": True, 
        "is_verified": True,
        "avatar_url": None,
        "bio": None
    }
    mock_user_orm.select.return_value.where.return_value = mock_query
    
    mocker.patch("app.middleware.auth.User", mock_user_orm)
    mocker.patch("app.middleware.auth.AuthService.decode_token", return_value=1)
    
    return mock_user_orm