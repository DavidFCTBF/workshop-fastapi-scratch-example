from strawberry import Schema

from manager.infrastructure.app.schemas.employee.mutation import Mutation
from manager.infrastructure.app.schemas.employee.query import Query



schema = Schema(query=Query, mutation=Mutation)

