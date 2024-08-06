from typing import Optional

from pydantic import NonNegativeInt
from sqlalchemy import ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from core.show.schema.show import ShowSchema, ShowState, ShowClass
from database.sqlalchemy.database import Base
from utils.types import ID, ShowName


class ShowORM(Base):
    id: Mapped[NonNegativeInt] = mapped_column(primary_key=True)
    species_id: Mapped[Optional[NonNegativeInt]] = mapped_column(ForeignKey(column="species.id"), nullable=True)
    breed_id: Mapped[Optional[NonNegativeInt]] = mapped_column(ForeignKey(column="breed.id"), nullable=True)
    state: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    show_class: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    is_multi_breed: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def to_schema(self) -> ShowSchema:
        return ShowSchema(
            id=ID(self.id),
            species_id=ID(self.species_id),
            breed_id=ID(self.breed_id),
            state=ShowState(self.state),
            show_class=ShowClass(self.show_class),
            name=ShowName(self.name),
            is_multi_breed=self.is_multi_breed
        )
