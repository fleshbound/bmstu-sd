from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.group.schema.group import GroupSchema
from repository.sqlalchemy.database.database import Base
from core.utils.types import ID, GroupName


class GroupORM(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    def to_schema(self) -> GroupSchema:
        return GroupSchema(
            id=ID(self.id),
            name=GroupName(self.name)
        )
