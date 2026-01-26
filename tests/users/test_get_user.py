import pytest
from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock
from polyfactory.factories.msgspec_factory import MsgspecFactory
from app.dtos.user import UserResponseDTO

class UserResponseDTOFactory(MsgspecFactory[UserResponseDTO]):
    pass

@pytest.mark.asyncio
async def test_get_user_profile(client, unique_username, mocker):
    # Controller uses User.select().where(...).first()
    # Patch app.controllers.user.User
    
    mock_user_orm = MagicMock()
    mock_query = AsyncMock()
    # Mock return dict
    mock_query.first.return_value = {
        "id": 1, 
        "username": unique_username, 
        "email": "test@example.com", 
        "avatar_url": None, 
        "bio": None,
        "is_active": True, 
        "is_verified": True
    }
    mock_user_orm.select.return_value.where.return_value = mock_query
    
    mocker.patch("app.controllers.user.User", mock_user_orm)

    # Execute
    response = await client.get(f"/api/users/{unique_username}")
    
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["username"] == unique_username
    
    mock_user_orm.select.assert_called()

@pytest.mark.asyncio
async def test_get_user_not_found(client, mocker):
    mock_user_orm = MagicMock()
    mock_query = AsyncMock()
    mock_query.first.return_value = None # Not found
    mock_user_orm.select.return_value.where.return_value = mock_query
    
    mocker.patch("app.controllers.user.User", mock_user_orm)
    
    response = await client.get("/api/users/nonexistent_user")
    assert response.status_code == HTTPStatus.NOT_FOUND
