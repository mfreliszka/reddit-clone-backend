from msgspec import Struct
from .user import UserResponseDTO


class UserLoginResponseDTO(Struct):
    access_token: str
    token_type: str
    user: UserResponseDTO
