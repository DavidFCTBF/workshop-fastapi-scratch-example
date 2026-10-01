import strawberry
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column

from sqlalchemy.types import DateTime
from sqlalchemy.sql import func

@strawberry.type
class GenericModelSchema(BaseModel):
    id: int
    updated_date: datetime
    updated_by: str
    created_by: str
    created_date: datetime

    model_config = ConfigDict(from_attributes=True)


class GenericModelORM(MappedAsDataclass, DeclarativeBase, kw_only=True):
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    updated_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now()
    )
    updated_by: Mapped[str]
    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now()
    )
    created_by: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
