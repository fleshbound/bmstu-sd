from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.species.schema.species import SpeciesSchema
from repository.sqlalchemy.model.base import Base
from core.utils.types import ID, SpeciesName


class SpeciesORM(Base):
    __tablename__ = "species"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey(column="group.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)

    def to_schema(self) -> SpeciesSchema:
        return SpeciesSchema(
            id=ID(self.id),
            group_id=ID(self.group_id),
            name=SpeciesName(self.name)
        )
