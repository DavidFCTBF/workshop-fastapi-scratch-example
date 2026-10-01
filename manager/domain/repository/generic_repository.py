from abc import ABC, abstractmethod
from ..entities.generic_model import GenericModelSchema
from typing import List

class IGenericRepository(ABC):

    @abstractmethod
    async def create(self, model: GenericModelSchema) -> GenericModelSchema:
        pass

    @abstractmethod
    async def get_all(self, limit:int) -> List[GenericModelSchema]:
        pass