import os
from pathlib import Path

from dotenv import load_dotenv
from dependency_injector import containers, providers
from manager.infrastructure.di.database import PostgressDatabase
from manager.infrastructure.di.repository import Repository
from manager.infrastructure.di.app_service import AppService

_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.yml"
_ENV_PATH = Path(__file__).resolve().parents[3] / ".env"
_REQUIRED_ENV = (
    "POSTGRES_HOST",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_DB",
    "POSTGRES_PORT",
)

load_dotenv(_ENV_PATH)

_missing = [name for name in _REQUIRED_ENV if not os.environ.get(name)]
if _missing:
    raise RuntimeError(
        "Missing Postgres environment variables: "
        + ", ".join(_missing)
        + ". Copy .env.example to .env and set them."
    )


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()
    config.from_yaml(str(_CONFIG_PATH))

    databases = providers.Container(
        PostgressDatabase,
        host=config.postgre_sql.host,
        user=config.postgre_sql.user,
        password=config.postgre_sql.password,
        database=config.postgre_sql.database,
        port=config.postgre_sql.port

    )

    repositories = providers.Container(
        Repository,
        db=config.dummy.file,
        databases=databases
    )

    apps = providers.Container(
        AppService,
        repositories=repositories,
    )
