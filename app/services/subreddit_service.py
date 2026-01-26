from typing import Any
from litestar.exceptions import ClientException, NotFoundException
from app.models.subreddit import Subreddit
from app.dtos.subreddit import SubredditCreateDTO, SubredditResponseDTO


class SubredditService:
    """
    Service for handling subreddit operations.
    """

    async def create_subreddit(
        self, data: SubredditCreateDTO, owner_id: int
    ) -> SubredditResponseDTO:
        """
        Create a new subreddit.

        Args:
            data: The subreddit creation data.
            owner_id: The ID of the user creating the subreddit.

        Returns:
            SubredditResponseDTO: The created subreddit.

        Raises:
            ClientException: If the subreddit name already exists.
        """
        existing: dict[str, Any] | None = (
            await Subreddit.select().where(Subreddit.name == data.name).first()
        )
        if existing:
            raise ClientException(f"Subreddit '{data.name}' already exists")

        new_sub: Subreddit = Subreddit(
            name=data.name, description=data.description, owner=owner_id
        )
        await new_sub.save()

        return SubredditResponseDTO(
            id=new_sub.id,
            name=new_sub.name,
            description=new_sub.description,
            created_at=new_sub.created_at,
            owner_id=new_sub.owner,
        )

    async def get_all(self) -> list[SubredditResponseDTO]:
        """
        Get all subreddits.

        Returns:
            list[SubredditResponseDTO]: A list of all subreddits.
        """
        subreddits: list[dict[str, Any]] = await Subreddit.select().order_by(
            Subreddit.name
        )
        return [
            SubredditResponseDTO(
                id=sub["id"],
                name=sub["name"],
                description=sub["description"],
                created_at=sub["created_at"],
                owner_id=sub["owner"],
            )
            for sub in subreddits
        ]

    async def get_by_name(self, name: str) -> SubredditResponseDTO:
        """
        Get a subreddit by name.

        Args:
            name: The name of the subreddit.

        Returns:
            SubredditResponseDTO: The found subreddit.

        Raises:
            NotFoundException: If the subreddit does not exist.
        """
        sub: dict[str, Any] | None = (
            await Subreddit.select().where(Subreddit.name == name).first()
        )
        if not sub:
            raise NotFoundException(f"Subreddit '{name}' not found")

        return SubredditResponseDTO(
            id=sub["id"],
            name=sub["name"],
            description=sub["description"],
            created_at=sub["created_at"],
            owner_id=sub["owner"],
        )
