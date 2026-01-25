from typing import Any
from litestar import Controller, get, post, Request
from litestar.di import Provide
from litestar.exceptions import NotAuthorizedException, NotFoundException
from app.services.post_service import PostService
from app.dtos.post import PostCreateDTO, PostResponseDTO

class PostController(Controller):
    """
    Controller for handling post-related operations.
    """
    path = "/api"
    dependencies = {"post_service": Provide(PostService)}

    @post("/r/{subreddit:str}/posts")
    async def create_post(self, subreddit: str, data: PostCreateDTO, request: Request, post_service: PostService) -> PostResponseDTO:
        """
        Create a new post in a subreddit.

        Args:
            subreddit: The name of the subreddit.
            data: The post data.
            request: The request object.
            post_service: The injected post service.

        Returns:
            PostResponseDTO: The created post.

        Raises:
            NotAuthorizedException: If not authenticated.
            ClientException: If data validation fails.
        """
        user: dict[str, Any] | None = request.user
        if not user:
            raise NotAuthorizedException()
        
        # Ensure subreddit exists in payload matches URL or override it
        data.subreddit_name = subreddit
        
        return await post_service.create_post(data, author_id=int(user["id"]))

    @get("/posts/{post_id:int}")
    async def get_post(self, post_id: int, post_service: PostService) -> PostResponseDTO:
        """
        Get a specific post.
        
        Args:
            post_id: The ID of the post.
            post_service: The injected post service.

        Returns:
            PostResponseDTO: The post.
        """
        return await post_service.get_post(post_id)

    @get("/r/{subreddit:str}/posts")
    async def list_posts(self, subreddit: str, post_service: PostService) -> list[PostResponseDTO]:
        """
        List posts in a subreddit.

        Args:
            subreddit: The name of the subreddit.
            post_service: The injected post service.

        Returns:
            list[PostResponseDTO]: List of posts.
        """
        return await post_service.get_posts_by_subreddit(subreddit)
