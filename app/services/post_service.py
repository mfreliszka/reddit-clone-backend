from typing import Any
from litestar.exceptions import NotFoundException
from app.models.post import Post
from app.models.subreddit import Subreddit
from app.dtos.post import PostCreateDTO, PostResponseDTO

class PostService:
    """
    Service for handling post creation and retrieval.
    """
    async def create_post(self, data: PostCreateDTO, author_id: int) -> PostResponseDTO:
        """
        Create a new post in a subreddit.

        Args:
            data: The post data including title, content/url, and subreddit name.
            author_id: The ID of the author.

        Returns:
            PostResponseDTO: The created post.

        Raises:
            NotFoundException: If the subreddit does not exist.
        """
        # Find subreddit (using dict for type safety if needed, but Piccolo returns Row/dict)
        subreddit: dict[str, Any] | None = await Subreddit.select().where(Subreddit.name == data.subreddit_name).first()
        if not subreddit:
            raise NotFoundException(f"Subreddit '{data.subreddit_name}' not found")

        new_post: Post = Post(
            title=data.title,
            content=data.content,
            url=data.url,
            author=author_id,
            subreddit=subreddit["id"]
        )
        await new_post.save()

        return PostResponseDTO(
            id=new_post.id,
            title=new_post.title,
            content=new_post.content,
            url=new_post.url,
            created_at=new_post.created_at,
            author_id=new_post.author,
            subreddit_id=new_post.subreddit
        )

    async def get_post(self, post_id: int) -> PostResponseDTO:
        """
        Get a specific post by ID.

        Args:
            post_id: The ID of the post.

        Returns:
            PostResponseDTO: The requested post.

        Raises:
            NotFoundException: If the post does not exist.
        """
        post: dict[str, Any] | None = await Post.select().where(Post.id == post_id).first()
        if not post:
            raise NotFoundException("Post not found")

        return PostResponseDTO(
            id=post["id"],
            title=post["title"],
            content=post["content"],
            url=post["url"],
            created_at=post["created_at"],
            author_id=post["author"],
            subreddit_id=post["subreddit"]
        )
    
    async def get_posts_by_subreddit(self, subreddit_name: str) -> list[PostResponseDTO]:
        """
        Get all posts for a given subreddit.
        
        Args:
            subreddit_name: The name of the subreddit.

        Returns:
             list[PostResponseDTO]: List of posts.

        Raises:
            NotFoundException: If subreddit not found.
        """
        subreddit: dict[str, Any] | None = await Subreddit.select().where(Subreddit.name == subreddit_name).first()
        if not subreddit:
            raise NotFoundException(f"Subreddit '{subreddit_name}' not found")

        posts: list[dict[str, Any]] = await Post.select().where(
            Post.subreddit == subreddit["id"]
        ).order_by(Post.created_at, ascending=False)

        return [
            PostResponseDTO(
                id=p["id"],
                title=p["title"],
                content=p["content"],
                url=p["url"],
                created_at=p["created_at"],
                author_id=p["author"],
                subreddit_id=p["subreddit"]
            ) for p in posts
        ]
