import pytest
from http import HTTPStatus
from unittest.mock import AsyncMock
from polyfactory.factories.msgspec_factory import MsgspecFactory
from app.services.subreddit_service import SubredditService
from app.dtos.subreddit import SubredditResponseDTO

class SubredditResponseDTOFactory(MsgspecFactory[SubredditResponseDTO]):
    pass

@pytest.mark.asyncio
async def test_get_subreddit_by_name(client, mocker):
    # Mock
    mock_service_instance = AsyncMock(spec=SubredditService)
    expected_response = SubredditResponseDTOFactory.build(name="testsub")
    mock_service_instance.get_by_name.return_value = expected_response
    
    mocker.patch("app.controllers.subreddit.provide_subreddit_service", return_value=mock_service_instance)
    
    # Execute
    response = await client.get("/api/subreddits/testsub")
    
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["name"] == "testsub"
    
    mock_service_instance.get_by_name.assert_called_once_with("testsub")

@pytest.mark.asyncio
async def test_get_subreddit_not_found(client, mocker):
    from litestar.exceptions import NotFoundException
    
    mock_service_instance = AsyncMock(spec=SubredditService)
    mock_service_instance.get_by_name.side_effect = NotFoundException("Sub not found")
    
    mocker.patch("app.controllers.subreddit.SubredditService", return_value=mock_service_instance)
    
    response = await client.get("/api/subreddits/nonexistent")
    assert response.status_code == HTTPStatus.NOT_FOUND
