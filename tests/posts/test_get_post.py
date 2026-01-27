import pytest
from http import HTTPStatus
from unittest.mock import AsyncMock
from polyfactory.factories.msgspec_factory import MsgspecFactory
from app.services.post_service import PostService
from app.dtos.post import PostResponseDTO

class PostResponseDTOFactory(MsgspecFactory[PostResponseDTO]):
    pass

@pytest.mark.asyncio
async def test_get_post(client, mocker):
    # Mock
    mock_service_instance = AsyncMock(spec=PostService)
    expected_response = PostResponseDTOFactory.build(id=123)
    mock_service_instance.get_post.return_value = expected_response
    
    mocker.patch("app.controllers.post.provide_post_service", return_value=mock_service_instance)
    
    # Execute
    response = await client.get("/api/posts/123")
    
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["id"] == 123
    
    mock_service_instance.get_post.assert_called_once_with(123)

@pytest.mark.asyncio
async def test_get_post_not_found(client, mocker):
    from litestar.exceptions import NotFoundException
    
    mock_service_instance = AsyncMock(spec=PostService)
    mock_service_instance.get_post.side_effect = NotFoundException("Post not found")
    
    mocker.patch("app.controllers.post.PostService", return_value=mock_service_instance)
    
    response = await client.get("/api/posts/999")
    assert response.status_code == HTTPStatus.NOT_FOUND
