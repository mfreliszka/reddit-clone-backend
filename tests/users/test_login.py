import pytest
from http import HTTPStatus
from unittest.mock import AsyncMock
from polyfactory.factories.msgspec_factory import MsgspecFactory
from app.services.user_service import UserService
from app.dtos.auth import UserLoginResponseDTO
from app.dtos.user import UserLoginDTO
from app.models.user import User

class UserLoginDTOFactory(MsgspecFactory[UserLoginDTO]):
    pass

class UserLoginResponseDTOFactory(MsgspecFactory[UserLoginResponseDTO]):
    pass

@pytest.mark.asyncio
async def test_login_user(client, mocker):
    # Mock
    mock_service_instance = AsyncMock(spec=UserService)
    
    # Data
    payload = UserLoginDTOFactory.build()
    expected_token = UserLoginResponseDTOFactory.build()
    
    mock_service_instance.authenticate_user.return_value = expected_token
    
    mocker.patch("app.controllers.user.provide_user_service", return_value=mock_service_instance)

    response = await client.post(
        "/api/users/login",
        json={"username": payload.username, "password": payload.password},
    )

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["access_token"] == expected_token.access_token
    
    mock_service_instance.authenticate_user.assert_called_once() # Args match might fail on DTO equality

@pytest.mark.asyncio
async def test_login_invalid_password(client, mocker):
    from litestar.exceptions import NotAuthorizedException
    
    mock_service = AsyncMock(spec=UserService)
    mock_service.authenticate_user.side_effect = NotAuthorizedException("Invalid credentials")
    
    mocker.patch("app.controllers.user.provide_user_service", return_value=mock_service)
    
    response = await client.post(
        "/api/users/login",
        json={"username": "user", "password": "wrong"},
    )
    
    assert response.status_code == HTTPStatus.UNAUTHORIZED
