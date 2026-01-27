import os
from piccolo.conf.apps import AppConfig
from app.models.user import User
from app.models.subreddit import Subreddit
from app.models.post import Post

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

APP_CONFIG = AppConfig(
    app_name="app",
    migrations_folder_path=os.path.join(CURRENT_DIRECTORY, "migrations"),
    table_classes=[User, Subreddit, Post],
    migration_dependencies=[],
    commands=[],
)
