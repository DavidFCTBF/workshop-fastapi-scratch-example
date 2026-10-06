from contextlib import asynccontextmanager
from fastapi import FastAPI
from ..di.container import Container
from strawberry.fastapi import GraphQLRouter
from dependency_injector.wiring import Provide, inject

import psycopg
from psycopg.sql import SQL, Identifier

from .graphql_schema import schema
from strawberry.printer import print_schema



def ensure_database_exists(db_url: str):
    """Parses a database URL, connects to default 'postgres' db,
    and creates the target DB if it does not already exist.
    """
    # Parse the target connection string
    # Expected format: postgresql+psycopg://user:pass@host:port/target_db
    conn_info = psycopg.conninfo.make_conninfo(
        db_url.replace("postgresql+psycopg://", "postgresql://")
    )

    # Extract target DB name and switch connection target to 'postgres'
    parsed = psycopg.conninfo.conninfo_to_dict(conn_info)
    target_db = parsed.pop("dbname", None)
    parsed["dbname"] = "postgres"  # Default admin DB

    if not target_db:
        return

    # Connect to the default 'postgres' DB
    with psycopg.connect(**parsed, autocommit=True) as conn:
        with conn.cursor() as cur:
            # Check if target database exists
            cur.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s;",
                (target_db,)
            )
            exists = cur.fetchone()

            # Create target DB if missing
            if not exists:
                cur.execute(SQL("CREATE DATABASE {}").format(Identifier(target_db)))

def generate_schema(schema):
    printed_schema = print_schema(schema)
    with open("employee_schema.graphql", "w") as f:
        f.write(printed_schema)

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

    postgres = container.databases.postgre_sql()
    ensure_database_exists(
        postgres.connection_url.render_as_string(hide_password=False)
    )

    postgres.connect_to_database()

    async with postgres.sesion_maker.kw['bind'].begin() as conn:
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

generate_schema(schema)
