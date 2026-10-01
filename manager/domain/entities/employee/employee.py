import strawberry

from ..generic_model import GenericModelORM, GenericModelSchema
from sqlalchemy.orm import Mapped, mapped_column


@strawberry.type
class EmployeeSchema(GenericModelSchema):
    id: int
    first_name: str
    email: str



class EmployeeORM(GenericModelORM):
    __tablename__ = "hr.employee"

    first_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
