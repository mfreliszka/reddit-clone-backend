from msgspec import Struct
from typing import Any
from datetime import datetime

class SubredditCreateDTO(Struct):
    name: str
    description: str | None = None

class SubredditResponseDTO(Struct):
    id: int
    name: str
    description: str | None
    created_at: datetime
    owner_id: int
