from datetime import datetime
from litestar import Controller, get, post, Request
from litestar.di import Provide
from litestar.exceptions import NotFoundException, NotAuthorizedException
from app.dtos.user import UserRegisterDTO, UserLoginDTO, UserResponseDTO
from app.dtos.auth import UserLoginResponseDTO
from app.services.user_service import UserService
from app.models.user import User

class UserController(Controller):
    """
    Controller for handling user-related operations such as registration, login, and profile retrieval.
    """
    path = "/api/users"
    dependencies = {"user_service": Provide(UserService)}

    @post("/register")
    async def register(self, data: UserRegisterDTO, user_service: UserService) -> UserResponseDTO:
        """
        Register a new user.

        Args:
            data: The user registration data.
            user_service: The injected user service.

        Returns:
            UserResponseDTO: The created user's profile.
        """
        return await user_service.create_user(data)

    @post("/login")
    async def login(self, data: UserLoginDTO, user_service: UserService) -> UserLoginResponseDTO:
        """
        Authenticate a user and return a JWT token.

        Args:
            data: The user login credentials.
            user_service: The injected user service.

        Returns:
            UserLoginResponseDTO: The authentication response containing the access token.
        """
        return await user_service.authenticate_user(data)

    @get("/me")
    async def get_me(self, request: Request) -> UserResponseDTO:
        """
        Get the authenticated user's profile.

        Args:
            request: The incoming request containing the user context.

        Returns:
            UserResponseDTO: The authenticated user's profile.

        Raises:
            NotAuthorizedException: If the user is referenced but not found in context (should catch middleware issues).
        """
        user: dict[str, str | int | bool | datetime | None] | None = request.user
        if not user:
            raise NotAuthorizedException()
            
        return UserResponseDTO(
            id=user["id"],
            username=user["username"],
            email=user["email"],
            avatar_url=user["avatar_url"],
            bio=user["bio"],
            is_active=user["is_active"],
            is_verified=user["is_verified"],
        )

    @get("/{username:str}")
    async def get_user(self, username: str) -> UserResponseDTO:
        """
        Get a user's public profile by username.

        Args:
            username: The username to search for.

        Returns:
            UserResponseDTO: The user's public profile.

        Raises:
            NotFoundException: If the user does not exist.
        """
        user: dict[str, str | int | bool | datetime | None] | None = await User.select().where(User.username == username).first()
        if not user:
            raise NotFoundException("User not found")
        
        return UserResponseDTO(
            id=user["id"],
            username=user["username"],
            email=user["email"],
            avatar_url=user["avatar_url"],
            bio=user["bio"],
            is_active=user["is_active"],
            is_verified=user["is_verified"],
        )

    # TODO: Helper to map User model to DTO if service methods aren't used for simple queries
