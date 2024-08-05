from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.group.schema.group import GroupSchema
from database.sqlalchemy.database import Base
from utils.types import ID, GroupName


class GroupORM(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    def to_schema(self) -> GroupSchema:
        return GroupSchema(
            id=ID(value=self.id),
            name=GroupName(value=self.name)
        )
