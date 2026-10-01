import strawberry
from strawberry.types import Info

from manager.infrastructure.app.schemas.employee.schema import GetEmployeeSchema, SetEmployeeSchema
from manager.application.employee.employee import EmployeeApp
from manager.domain.entities.employee.employee import EmployeeORM, EmployeeSchema

@strawberry.type
class Mutation:


    @strawberry.mutation
    async def create(self, info: Info, employee: SetEmployeeSchema) -> GetEmployeeSchema:
        employee_app: EmployeeApp = info.context['employee_app']
        employee_orm: EmployeeORM = await employee_app.create(employee)
        return GetEmployeeSchema.from_pydantic(
            EmployeeSchema.model_validate(employee_orm)
        )
