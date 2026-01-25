from piccolo.table import Table
from piccolo.columns import Varchar, Timestamp, Text, Serial, ForeignKey
from datetime import datetime
from app.models.user import User
from app.models.subreddit import Subreddit

class Post(Table):
    """
    Model representing a user submission (post) to a subreddit.
    """
    id = Serial(primary_key=True)
    title = Varchar(length=300)
    content = Text(null=True)
    url = Varchar(length=1000, null=True)
    created_at = Timestamp(default=datetime.now)
    author = ForeignKey(references=User)
    subreddit = ForeignKey(references=Subreddit)
