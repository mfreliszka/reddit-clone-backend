from piccolo.table import Table
from piccolo.columns import Varchar, Timestamp, Boolean, Text, Serial
from datetime import datetime

class User(Table, tablename="users"):
    """
    User model for authentication and profile management.
    """
    id = Serial(primary_key=True)
    username = Varchar(length=50, unique=True, index=True)
    email = Varchar(length=255, unique=True, index=True)
    password_hash = Varchar(length=255)
    avatar_url = Text(null=True)
    bio = Text(null=True)
    is_active = Boolean(default=True) 
    is_verified = Boolean(default=False)
    created_at = Timestamp(default=datetime.now)

    @property
    def check_password(self, password: str) -> bool:
        # Placeholder for password verification logic (e.g. Argon2)
        # This will be implemented in the AuthService
        pass
