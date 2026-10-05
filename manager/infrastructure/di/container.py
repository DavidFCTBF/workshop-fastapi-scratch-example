import os
from pathlib import Path

from dependency_injector import containers, providers
from manager.infrastructure.di.database import PostgressDatabase
from manager.infrastructure.di.repository import Repository
from manager.infrastructure.di.app_service import AppService

_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.yml"


def _postgres_env_overrides() -> dict:
    mapping = {
        "host": "POSTGRES_HOST",
        "user": "POSTGRES_USER",
        "password": "POSTGRES_PASSWORD",
        "database": "POSTGRES_DB",
        "port": "POSTGRES_PORT",
    }
    values = {
        key: os.environ[env_name]
        for key, env_name in mapping.items()
        if env_name in os.environ
    }
    if not values:
        return {}
    return {"postgre_sql": values}


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()
    config.from_yaml(str(_CONFIG_PATH))
    config.from_dict(_postgres_env_overrides())

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