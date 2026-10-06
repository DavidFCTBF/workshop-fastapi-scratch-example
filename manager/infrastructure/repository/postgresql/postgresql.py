from typing import AsyncGenerator, Any
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession




class PostgreSQL:
    sesion_maker: Any
    connection_url: URL

    def __init__(self, host: str, database: str, user: str, password: str, port: int) -> None:

        self.connection_url = URL.create(
            drivername="postgresql+psycopg",
            username=user,
            password=password,
            host=host,
            port=int(port),
            database=database
        )

    def connect_to_database(self):

        engine= create_async_engine(
            self.connection_url,
            echo=True,
        )

        self.sesion_maker = async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
            class_=AsyncSession
        )


    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.sesion_maker() as session:
            yield session



