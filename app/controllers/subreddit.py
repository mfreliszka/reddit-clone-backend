from typing import Any
from litestar import Controller, get, post, Request
from litestar.di import Provide
from litestar.exceptions import NotFoundException, NotAuthorizedException
from app.services.subreddit_service import SubredditService
from app.dtos.subreddit import SubredditCreateDTO, SubredditResponseDTO



def provide_subreddit_service() -> SubredditService:
    return SubredditService()


class SubredditController(Controller):
    """
    Controller for handling subreddit-related operations.
    """

    path = "/api/subreddits"
    dependencies = {"subreddit_service": Provide(lambda: provide_subreddit_service())}

    @post("/")
    async def create_subreddit(
        self,
        data: SubredditCreateDTO,
        request: Request,
        subreddit_service: SubredditService,
    ) -> SubredditResponseDTO:
        """
        Create a new subreddit.

        Args:
            data: The subreddit creation payload.
            request: The request object to retrieve the authenticated user.
            subreddit_service: The injected subreddit service.

        Returns:
            SubredditResponseDTO: The created subreddit.

        Raises:
            NotAuthorizedException: If the user is not authenticated.
        """
        user: dict[str, Any] | None = request.user
        if not user:
            raise NotAuthorizedException()

        return await subreddit_service.create_subreddit(data, owner_id=int(user["id"]))

    @get("/")
    async def get_all_subreddits(
        self, subreddit_service: SubredditService
    ) -> list[SubredditResponseDTO]:
        """
        List all subreddits.

        Args:
            subreddit_service: The injected subreddit service.

        Returns:
            list[SubredditResponseDTO]: A list of all subreddits.
        """
        return await subreddit_service.get_all()

    @get("/{name:str}")
    async def get_subreddit(
        self, name: str, subreddit_service: SubredditService
    ) -> SubredditResponseDTO:
        """
        Get a specific subreddit by name.

        Args:
            name: The name of the subreddit.
            subreddit_service: The injected subreddit service.

        Returns:
            SubredditResponseDTO: The requested subreddit.
        """
        return await subreddit_service.get_by_name(name)
