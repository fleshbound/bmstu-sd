from pydantic import NonNegativeInt, NonNegativeFloat, PositiveFloat
from sqlalchemy import ForeignKey, String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from internal.src.core.standard.schema.standard import StandardSchema
from internal.src.core.utils.types import ID, Height, Weight, Country, Length
from internal.src.repository.sqlalchemy.model.base import Base


class StandardORM(Base):
    __tablename__ = 'standard'

    id: Mapped[NonNegativeInt] = mapped_column(primary_key=True)
    breed_id: Mapped[NonNegativeInt] = mapped_column(ForeignKey(column='breed.id'))
    country: Mapped[str] = mapped_column(String, nullable=False)
    weight: Mapped[NonNegativeFloat] = mapped_column(Float, nullable=False)
    height: Mapped[NonNegativeFloat] = mapped_column(Float, nullable=False)
    has_defects: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_multi_color: Mapped[bool] = mapped_column(Boolean, nullable=False)
    length: Mapped[NonNegativeFloat] = mapped_column(Float, nullable=False)
    weight_delta_percent: Mapped[PositiveFloat] = mapped_column(Float, nullable=False)
    height_delta_percent: Mapped[PositiveFloat] = mapped_column(Float, nullable=False)
    length_delta_percent: Mapped[PositiveFloat] = mapped_column(Float, nullable=False)

    def to_schema(self) -> StandardSchema:
        return StandardSchema(
            id=ID(self.id),
            breed_id=ID(self.breed_id),
            country=Country(self.country),
            weight=Weight(self.weight),
            height=Height(self.height),
            has_defects=self.has_defects,
            is_multi_color=self.is_multi_color,
            length=Length(self.length),
            weight_delta_percent=Weight(self.weight_delta_percent),
            height_delta_percent=Height(self.height_delta_percent),
            length_delta_percent=Length(self.length_delta_percent)
        )
