from typing import Optional

from pydantic import NonNegativeInt
from sqlalchemy import ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from core.show.schema.show import ShowSchema, ShowStatus, ShowClass
from core.utils.types import ID, ShowName, Country
from repository.sqlalchemy.model.base import Base


class ShowORM(Base):
    __tablename__ = 'show'

    id: Mapped[NonNegativeInt] = mapped_column(primary_key=True)
    species_id: Mapped[Optional[NonNegativeInt]] = mapped_column(ForeignKey(column="species.id"), nullable=True)
    standard_id: Mapped[Optional[NonNegativeInt]] = mapped_column(ForeignKey(column="standard.id"), nullable=True)
    breed_id: Mapped[Optional[NonNegativeInt]] = mapped_column(ForeignKey(column="breed.id"), nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    show_class: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    is_multi_breed: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def to_schema(self) -> ShowSchema:
        standard_id = self.standard_id if self.standard_id is None else ID(self.standard_id)
        species_id = self.species_id if self.species_id is None else ID(self.species_id)
        breed_id = self.breed_id if self.breed_id is None else ID(self.breed_id)
        return ShowSchema(
            id=ID(self.id),
            species_id=species_id,
            breed_id=breed_id,
            country=Country(self.country),
            status=ShowStatus(self.status),
            show_class=ShowClass(self.show_class),
            standard_id=standard_id,
            name=ShowName(self.name),
            is_multi_breed=self.is_multi_breed
        )
