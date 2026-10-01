from dependency_injector import containers, providers
from manager.infrastructure.di.database import PostgressDatabase
from manager.infrastructure.di.repository import Repository
from manager.infrastructure.di.app_service import AppService

class Container(containers.DeclarativeContainer):

    config = providers.Configuration()
    config.from_yaml('/Users/david.flores/Documents/uv_example/rh/manager/config.yml')

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