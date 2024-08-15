from pydantic import NonNegativeInt
from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from core.show.schema.animalshow import AnimalShowSchema
from repository.sqlalchemy.database.database import Base
from core.utils.types import ID


class AnimalShowORM(Base):
    __tablename__ = 'animalshow'

    id: Mapped[NonNegativeInt] = mapped_column(primary_key=True)
    animal_id: Mapped[NonNegativeInt] = mapped_column(ForeignKey(column='animal.id'), nullable=False)
    show_id: Mapped[NonNegativeInt] = mapped_column(ForeignKey(column='show.id'), nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def to_schema(self) -> AnimalShowSchema:
        return AnimalShowSchema(
            id=ID(self.id),
            animal_id=ID(self.animal_id),
            show_id=ID(self.show_id),
            is_archived=self.is_archived
        )
