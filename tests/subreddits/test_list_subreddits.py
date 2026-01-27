import pytest
from http import HTTPStatus
from unittest.mock import AsyncMock
from polyfactory.factories.msgspec_factory import MsgspecFactory
from app.services.subreddit_service import SubredditService
from app.dtos.subreddit import SubredditResponseDTO

class SubredditResponseDTOFactory(MsgspecFactory[SubredditResponseDTO]):
    pass

@pytest.mark.asyncio
async def test_list_subreddits(client, mocker):
    # Mock Service
    mock_service_instance = AsyncMock(spec=SubredditService)
    expected_list = [SubredditResponseDTOFactory.build() for _ in range(2)]
    mock_service_instance.get_all.return_value = expected_list
    
    mocker.patch("app.controllers.subreddit.provide_subreddit_service", return_value=mock_service_instance)
    
    # Execute
    response = await client.get("/api/subreddits/")
    
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == expected_list[0].name
    
    mock_service_instance.get_all.assert_called_once()
