from msgspec import Struct
from datetime import datetime

class PostCreateDTO(Struct):
    title: str
    subreddit_name: str
    content: str | None = None
    url: str | None = None

class PostResponseDTO(Struct):
    id: int
    title: str
    content: str | None
    url: str | None
    created_at: datetime
    author_id: int
    subreddit_id: int
