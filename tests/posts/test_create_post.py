import pytest
from http import HTTPStatus
from unittest.mock import AsyncMock
from polyfactory.factories.msgspec_factory import MsgspecFactory
from app.services.post_service import PostService
from app.dtos.post import PostCreateDTO, PostResponseDTO

class PostCreateDTOFactory(MsgspecFactory[PostCreateDTO]):
    pass

class PostResponseDTOFactory(MsgspecFactory[PostResponseDTO]):
    pass

@pytest.mark.asyncio
async def test_create_post(client, mocker, mock_auth):
    # Data
    payload = PostCreateDTOFactory.build()
    expected_response = PostResponseDTOFactory.build(
        title=payload.title, 
        content=payload.content,
        subreddit_id=1
    )
    
    # Mock
    mock_service_instance = AsyncMock(spec=PostService)
    mock_service_instance.create_post.return_value = expected_response
    
    mocker.patch("app.controllers.post.provide_post_service", return_value=mock_service_instance)
    
    # Execute
    token = "valid_token"
    sub_name = payload.subreddit_name
    
    response = await client.post(
        f"/api/r/{sub_name}/posts",
        json={
            "title": payload.title,
            "subreddit_name": payload.subreddit_name,
            "content": payload.content,
            "url": payload.url
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["title"] == payload.title
    
    # Verify Service Call
    mock_service_instance.create_post.assert_called_once()
