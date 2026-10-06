import os
from pathlib import Path

from dependency_injector import containers, providers
from manager.infrastructure.di.database import PostgressDatabase
from manager.infrastructure.di.repository import Repository
from manager.infrastructure.di.app_service import AppService

_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.yml"
_REQUIRED_ENV = (
    "GALILEO_HR_MANAGER_POSTGRES_HOST",
    "GALILEO_HR_MANAGER_POSTGRES_USER",
    "GALILEO_HR_MANAGER_POSTGRES_PASSWORD",
    "GALILEO_HR_MANAGER_POSTGRES_DB",
    "GALILEO_HR_MANAGER_POSTGRES_PORT",
)

_missing = [name for name in _REQUIRED_ENV if not os.environ.get(name)]
if _missing:
    raise RuntimeError(
        "Missing Postgres environment variables: "
        + ", ".join(_missing)
        + ". Export them in the shell before starting the app."
    )

if (
    Path("/.dockerenv").is_file()
    and os.environ.get("GALILEO_HR_MANAGER_POSTGRES_HOST") in {"localhost", "127.0.0.1"}
):
    os.environ["GALILEO_HR_MANAGER_POSTGRES_HOST"] = "host.docker.internal"


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
