from datetime import datetime
from litestar.connection import ASGIConnection
from litestar.middleware.authentication import AuthenticationResult, AbstractAuthenticationMiddleware
from litestar.exceptions import NotAuthorizedException
from app.services.auth_service import AuthService
from app.models.user import User

class JWTAuthenticationMiddleware(AbstractAuthenticationMiddleware):
    """
    Middleware for handling JWT Bearer token authentication.
    
    This middleware extracts the Bearer token from the Authorization header,
    validates it, and attaches the authenticated user to the request scope.
    """
    async def authenticate_request(self, connection: ASGIConnection) -> AuthenticationResult:
        """
        Authenticate the incoming request using a JWT token.

        Args:
            connection: The ASGI connection object.

        Returns:
            AuthenticationResult: The result containing the user and auth token.
        
        Raises:
            NotAuthorizedException: If the token is invalid or malformed.
        """
        auth_header: str | None = connection.headers.get("Authorization")
        if not auth_header:
            return AuthenticationResult(user=None, auth=None)

        try:
            scheme: str
            token: str
            scheme, token = auth_header.split(" ")
            if scheme.lower() != "bearer":
                 raise NotAuthorizedException("Invalid authentication scheme")
        except ValueError:
             raise NotAuthorizedException("Invalid authorization header format")

        auth_service: AuthService = AuthService()
        user_id: int | None = auth_service.decode_token(token)
        
        if not user_id:
             raise NotAuthorizedException("Invalid or expired token")

        # We return a simple user object or dictionary. 
        # For performance, maybe just ID, but fetching user ensures existence.
        user: dict[str, str | int | bool | datetime | None] | None = await User.select().where(User.id == user_id).first()
        if not user:
            raise NotAuthorizedException("User not found")

        return AuthenticationResult(user=user, auth=token)
