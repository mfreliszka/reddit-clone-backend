import jwt
import datetime
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from litestar.exceptions import PermissionDeniedException

ph = PasswordHasher()
SECRET_KEY = "super-secret-key-change-me"  # TODO: Move to env var
ALGORITHM = "HS256"


class AuthService:
    """
    Service for handling authentication-related security operations including
    password hashing (Argon2) and JWT token management.
    """

    def hash_password(self, password: str) -> str:
        """
        Hash a plaintext password using Argon2.

        Args:
            password: The plaintext password to hash.

        Returns:
            str: The hashed password string.
        """
        return ph.hash(password)

    def verify_password(self, hashed: str, password: str) -> bool:
        """
        Verify a password against its hash.

        Args:
            hashed: The stored password hash.
            password: The plaintext password to verify.

        Returns:
            bool: True if the password matches the hash, False otherwise.
        """
        try:
            ph.verify(hashed, password)
            return True
        except VerifyMismatchError:
            return False

    def needs_rehash(self, hashed: str) -> bool:
        """
        Check if a password hash needs to be regenerated (e.g. security parameters changed).

        Args:
            hashed: The current password hash.

        Returns:
            bool: True if rehashing is required.
        """
        return ph.check_needs_rehash(hashed)

    def create_token(self, user_id: int) -> str:
        """
        Create a new JWT access token for a user.

        Args:
            user_id: The ID of the user to encode in the token.

        Returns:
            str: The encoded JWT token string.
        """
        payload: dict[str, str | float | int | datetime.datetime] = {
            "sub": str(user_id),
            "exp": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(hours=24),
            "iat": datetime.datetime.now(datetime.timezone.utc),
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def decode_token(self, token: str) -> int | None:
        """
        Decode and validate a JWT token.

        Args:
            token: The JWT token string to decode.

        Returns:
            int | None: The user ID from the token subject if valid, None otherwise.
        """
        try:
            payload: dict[str, str | float | int] = jwt.decode(
                token, SECRET_KEY, algorithms=[ALGORITHM]
            )
            return int(payload["sub"])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None
