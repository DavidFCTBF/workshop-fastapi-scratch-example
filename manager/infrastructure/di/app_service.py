from dependency_injector import containers, providers
from manager.application.employee.employee import EmployeeApp

class AppService(containers.DeclarativeContainer):
    repositories = providers.DependenciesContainer()

    employee_app = providers.Factory(
        EmployeeApp,
        repositories.employee_repository
    )
