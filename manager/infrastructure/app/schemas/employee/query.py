import strawberry
from strawberry.types import Info
from typing import List

from manager.infrastructure.app.schemas.employee.schema import GetEmployeeSchema
from manager.application.employee.employee import EmployeeApp
from manager.domain.entities.employee.employee import EmployeeORM, EmployeeSchema

@strawberry.type
class Query:


    @strawberry.field
    async def get_all(self, info: Info) -> List[GetEmployeeSchema]:
        employee_app: EmployeeApp = info.context['employee_app']
        employee_list: List[EmployeeORM] = await employee_app.get_all()

        return [
            GetEmployeeSchema.from_pydantic(EmployeeSchema.model_validate(employee_orm))
            for employee_orm in employee_list
        ]

