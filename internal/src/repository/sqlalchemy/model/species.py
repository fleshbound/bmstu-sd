from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from internal.src.core.species.schema.species import SpeciesSchema
from internal.src.core.utils.types import ID, SpeciesName
from internal.src.repository.sqlalchemy.model.base import Base


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
