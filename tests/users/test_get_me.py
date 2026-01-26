import pytest
from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock
from polyfactory.factories.msgspec_factory import MsgspecFactory
from app.dtos.user import UserResponseDTO

class UserResponseDTOFactory(MsgspecFactory[UserResponseDTO]):
    pass

@pytest.mark.asyncio
async def test_get_me_authenticated(client, unique_username, unique_email, mocker, mock_auth):
    # Data
    # mock_auth sets username="testuser"
    
    # Execute
    token = "fake_token"
    response = await client.get(
        "/api/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    # mock_auth returns id=1, username="testuser"
    assert data["username"] == "testuser"
    assert data["id"] == 1


@pytest.mark.asyncio
async def test_get_me_unauthenticated(client):
    # No token, middleware (not mocked here? verify scope)
    # If mock_auth is NOT requested, middleware runs normally.
    # Without Auth header, it returns None user -> 401
    response = await client.get("/api/users/me")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
