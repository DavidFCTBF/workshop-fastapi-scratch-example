from dataclasses import dataclass
from manager.domain.entities.employee.employee import EmployeeSchema, EmployeeORM
from manager.domain.repository.generic_repository import IGenericRepository
from typing import List


@dataclass
class EmployeeApp:
    _repository : IGenericRepository

    async def create(self, employee: EmployeeSchema) -> EmployeeORM:
        return await self._repository.create(employee)

    async def get_all(self) -> List[EmployeeORM]:
        return await self._repository.get_all(100)