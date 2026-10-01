from contextlib import asynccontextmanager
from fastapi import FastAPI
from ..di.container import Container
from strawberry.fastapi import GraphQLRouter
from dependency_injector.wiring import Provide, inject

from .graphql_schema import schema


@inject
async def get_schema_context(
    employee_app=Provide[Container.apps.employee_app],
):
    return {
        "employee_app": employee_app
    }

container = Container()
container.wire(modules=[__name__])

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Fetch your engine from the container
    db = container.databases.postgre_sql()

    # 2. Tell SQLAlchemy to create all tables if they don't exist
    async with db.sesion_maker.kw['bind'].begin() as conn:
        # Import your declarative base (where EmployeeORM inherits from)
        from manager.domain.entities.generic_model import GenericModelORM
        await conn.run_sync(GenericModelORM.metadata.create_all)

    yield  # The app runs while yielded


app = FastAPI(title="RH", lifespan=lifespan)
#app.include_router(employee_router)


@app.get("/")
def health():
    return "Todo fino filipino"




graphql_app = GraphQLRouter(schema, context_getter=get_schema_context)
app.include_router(graphql_app, prefix="/graphql")