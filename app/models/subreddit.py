from piccolo.table import Table
from piccolo.columns import Varchar, Timestamp, Text, Serial, ForeignKey
from datetime import datetime
from app.models.user import User

class Subreddit(Table):
    """
    Model representing a community (subreddit).
    """
    id = Serial(primary_key=True)
    name = Varchar(length=50, unique=True, index=True)
    description = Text(null=True)
    created_at = Timestamp(default=datetime.now)
    owner = ForeignKey(references=User)
