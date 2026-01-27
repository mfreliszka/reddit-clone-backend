import pytest
from http import HTTPStatus
from unittest.mock import AsyncMock
from polyfactory.factories.msgspec_factory import MsgspecFactory
from app.services.user_service import UserService
from app.dtos.user import UserRegisterDTO, UserResponseDTO

# Factory for creating test data
class UserRegisterDTOFactory(MsgspecFactory[UserRegisterDTO]):
    pass

class UserResponseDTOFactory(MsgspecFactory[UserResponseDTO]):
    pass

@pytest.mark.asyncio
async def test_register_user(client, mocker):
    # Prepare Mock
    mock_service_instance = AsyncMock(spec=UserService)
    
    # Data
    payload = UserRegisterDTOFactory.build()
    expected_response = UserResponseDTOFactory.build()
    
    # Setup Mock return
    mock_service_instance.create_user.return_value = expected_response
    
    # Patch the Provider Function
    mocker.patch("app.controllers.user.provide_user_service", return_value=mock_service_instance)
    
    # Execute
    response = await client.post(
        "/api/users/register",
        json={
            "username": payload.username,
            "email": payload.email,
            "password": payload.password
        },
    )

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    
    # Verify Mock Interaction
    mock_service_instance.create_user.assert_called_once()
    
    # Verify Response matches Mock output
    assert data["username"] == expected_response.username
    assert data["id"] == expected_response.id
