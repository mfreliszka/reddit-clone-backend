import pytest
from http import HTTPStatus
from unittest.mock import AsyncMock
from polyfactory.factories.msgspec_factory import MsgspecFactory
from app.services.subreddit_service import SubredditService
from app.dtos.subreddit import SubredditCreateDTO, SubredditResponseDTO

class SubredditCreateDTOFactory(MsgspecFactory[SubredditCreateDTO]):
    pass

class SubredditResponseDTOFactory(MsgspecFactory[SubredditResponseDTO]):
    pass

@pytest.mark.asyncio
async def test_create_subreddit(client, mocker, mock_auth):
    # Data
    payload = SubredditCreateDTOFactory.build()
    expected_response = SubredditResponseDTOFactory.build(name=payload.name, description=payload.description)
    
    # Mock Service
    mock_service_instance = AsyncMock(spec=SubredditService)
    mock_service_instance.create_subreddit.return_value = expected_response
    
    mocker.patch("app.controllers.subreddit.provide_subreddit_service", return_value=mock_service_instance)
    
    # Execute
    token = "valid_token"
    response = await client.post(
        "/api/subreddits/",
        json={"name": payload.name, "description": payload.description},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["name"] == payload.name
    
    # Verify Service Call
    mock_service_instance.create_subreddit.assert_called_once()
    # verify owner_id=1


@pytest.mark.asyncio
async def test_create_duplicate_subreddit(client, mocker, mock_auth):
    from litestar.exceptions import ClientException
    
    # Data
    payload = SubredditCreateDTOFactory.build()
    
    # Mock Service Error
    mock_service_instance = AsyncMock(spec=SubredditService)
    mock_service_instance.create_subreddit.side_effect = ClientException("Subreddit already exists")
    
    mocker.patch("app.controllers.subreddit.provide_subreddit_service", return_value=mock_service_instance)
    
    # Execute
    token = "valid_token"
    response = await client.post(
        "/api/subreddits/",
        json={"name": payload.name, "description": payload.description},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == HTTPStatus.BAD_REQUEST
