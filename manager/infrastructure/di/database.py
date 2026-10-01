from dependency_injector import containers, providers
from manager.infrastructure.repository.postgresql.manager_postgresql import PostgreSQL

class PostgressDatabase(containers.DeclarativeContainer):
    host = providers.Dependency()
    database = providers.Dependency()
    user = providers.Dependency()
    password = providers.Dependency()
    port = providers.Dependency()

    postgre_sql = providers.Singleton(
        PostgreSQL,
        host=host,
        database=database,
        user=user,
        password=password,
        port=port,
    )
