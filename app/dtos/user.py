from msgspec import Struct


class UserRegisterDTO(Struct):
    username: str
    email: str
    password: str
    avatar_url: str | None = None
    bio: str | None = None

class UserLoginDTO(Struct):
    username: str
    password: str

class UserResponseDTO(Struct):
    id: int
    username: str
    email: str
    is_active: bool
    is_verified: bool
    avatar_url: str | None = None
    bio: str | None = None
