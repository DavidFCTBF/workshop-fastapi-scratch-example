import strawberry
from manager.domain.entities.employee.employee import EmployeeSchema


@strawberry.experimental.pydantic.type(model=EmployeeSchema, all_fields=True)
class GetEmployeeSchema: pass

@strawberry.experimental.pydantic.input(model=EmployeeSchema)
class SetEmployeeSchema:
    first_name: strawberry.auto
    email: strawberry.auto