import pytest
from http import HTTPStatus
from unittest.mock import AsyncMock
from polyfactory.factories.msgspec_factory import MsgspecFactory
from app.services.post_service import PostService
from app.dtos.post import PostResponseDTO

class PostResponseDTOFactory(MsgspecFactory[PostResponseDTO]):
    pass

@pytest.mark.asyncio
async def test_list_posts_in_subreddit(client, mocker):
    # Mock
    mock_service_instance = AsyncMock(spec=PostService)
    expected_list = [PostResponseDTOFactory.build() for _ in range(2)]
    mock_service_instance.get_posts_by_subreddit.return_value = expected_list
    
    mocker.patch("app.controllers.post.provide_post_service", return_value=mock_service_instance)
    
    # Execute
    sub_name = "testsub"
    response = await client.get(f"/api/r/{sub_name}/posts")
    
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == expected_list[0].title
    
    mock_service_instance.get_posts_by_subreddit.assert_called_once_with(sub_name)
