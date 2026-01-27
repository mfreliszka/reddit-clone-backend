from datetime import datetime
from app.services.auth_service import AuthService
from app.dtos.auth import UserLoginResponseDTO
from app.models.user import User
from app.dtos.user import UserRegisterDTO, UserLoginDTO, UserResponseDTO
from litestar.exceptions import (
    ClientException,
    NotFoundException,
    PermissionDeniedException,
)

auth_service = AuthService()


class UserService:
    """
    Service for handling user business logic including creation, authentication, and retrieval.
    """

    async def create_user(self, data: UserRegisterDTO) -> UserResponseDTO:
        """
        Create a new user in the database.

        Args:
            data: The registration data.

        Returns:
            UserResponseDTO: The created user's data.

        Raises:
            ClientException: If the username or email already exists.
        """
        existing_user: dict[str, str | int | bool | datetime | None] | None = (
            await User.select()
            .where((User.username == data.username) | (User.email == data.email))
            .first()
        )

        if existing_user:
            raise ClientException("Username or email already exists")

        hashed_password: str = auth_service.hash_password(data.password)

        new_user: User = User(
            username=data.username,
            email=data.email,
            password_hash=hashed_password,
            avatar_url=data.avatar_url,
            bio=data.bio,
        )
        await new_user.save()

        return UserResponseDTO(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email,
            avatar_url=new_user.avatar_url,
            bio=new_user.bio,
            is_active=new_user.is_active,
            is_verified=new_user.is_verified,
        )

    async def authenticate_user(self, data: UserLoginDTO) -> UserLoginResponseDTO:
        """
        Authenticate a user and generate an access token.

        Args:
            data: The login credentials.

        Returns:
            UserLoginResponseDTO: The response correctly containing the JWT token.

        Raises:
            NotFoundException: If the username is not found.
            PermissionDeniedException: If the password is incorrect.
        """
        user: dict[str, str | int | bool | datetime | None] | None = (
            await User.select().where(User.username == data.username).first()
        )
        if not user:
            raise NotFoundException("User not found")

        if not auth_service.verify_password(user["password_hash"], data.password):
            raise PermissionDeniedException("Invalid password")

        if auth_service.needs_rehash(user["password_hash"]):
            new_hash: str = auth_service.hash_password(data.password)
            await User.update({User.password_hash: new_hash}).where(
                User.id == user["id"]
            )

        token: str = auth_service.create_token(user["id"])

        user_dto: UserResponseDTO = UserResponseDTO(
            id=user["id"],
            username=user["username"],
            email=user["email"],
            avatar_url=user["avatar_url"],
            bio=user["bio"],
            is_active=user["is_active"],
            is_verified=user["is_verified"],
        )

        return UserLoginResponseDTO(
            access_token=token, token_type="Bearer", user=user_dto
        )
