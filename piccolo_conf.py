from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine
import os

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "reddit_clone")
DB_USER = os.environ.get("DB_USER", "postgres_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres_password")

# Using PostgresEngine with asyncpg
DB = PostgresEngine(
    config={
        "host": DB_HOST,
        "database": DB_NAME,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "port": int(DB_PORT),
    }
)

APP_REGISTRY = AppRegistry(apps=["app.piccolo_app"])
