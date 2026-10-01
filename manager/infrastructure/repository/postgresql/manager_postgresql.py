from typing import List
from dataclasses import asdict
from .postgresql import PostgreSQL
from manager.domain.entities.generic_model import GenericModelSchema
from manager.domain.repository.generic_repository import IGenericRepository
from sqlalchemy import select

class GenericRepository(IGenericRepository):

    def __init__(self, postgre_sql_session: PostgreSQL, model: GenericModelSchema):
        self.db = postgre_sql_session
        self.orm_model = model


    async def create(self, ir_model: GenericModelSchema) -> GenericModelSchema:
        # 1. Convert Strawberry dataclass input to a dictionary
        data_dict = asdict(ir_model)

        # 2. Filter out None values manually (replacing exclude_none=True)
        data_dict = {k: v for k, v in data_dict.items() if v is not None}
        data_dict.update({'updated_by': 'system', 'created_by': 'system'})  # Add default values for updated_by and created_by
        # 3. Pass kwargs to ORM model
        new_orm_obj = self.orm_model(**data_dict)
        self.db.add(new_orm_obj)
        try:
            await self.db.commit()
            await self.db.refresh(new_orm_obj)
            return new_orm_obj
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_all(self, limit:int) -> List[GenericModelSchema]:
        stmt = select(self.orm_model).limit(limit)
        aux = await self.db.execute(stmt)
        return list(aux.scalars().all())


