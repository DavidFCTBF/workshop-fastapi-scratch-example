from dependency_injector import containers, providers
from manager.infrastructure.repository.postgresql.manager_postgresql import GenericRepository
from manager.domain.entities.employee.employee import EmployeeORM

async def init_session(db_client):
    async for session in db_client.get_db():
        yield session

class Repository(containers.DeclarativeContainer):
    db = providers.Dependency()
    databases = providers.DependenciesContainer()


    db_session = providers.Resource(
        init_session,
        db_client=databases.postgre_sql
    )

    employee_repository = providers.Factory(
        GenericRepository,
        model=EmployeeORM,
        postgre_sql_session=db_session
    )

