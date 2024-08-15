from pydantic import NonNegativeInt, NonNegativeFloat, PositiveFloat
from sqlalchemy import ForeignKey, String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from core.standard.schema.standard import StandardSchema
from database.sqlalchemy.database import Base
from utils.types import ID, ProlixityIndex, Height, Weight, Country


class StandardORM(Base):
    __tablename__ = 'standard'

    id: Mapped[NonNegativeInt] = mapped_column(primary_key=True)
    breed_id: Mapped[NonNegativeInt] = mapped_column(ForeignKey(column='breed.id'))
    country: Mapped[str] = mapped_column(String, nullable=False)
    weight: Mapped[NonNegativeFloat] = mapped_column(Float, nullable=False)
    height: Mapped[NonNegativeFloat] = mapped_column(Float, nullable=False)
    has_defects: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_multi_color: Mapped[bool] = mapped_column(Boolean, nullable=False)
    prolixity_index: Mapped[NonNegativeFloat] = mapped_column(Float, nullable=False)
    weight_delta_percent: Mapped[PositiveFloat] = mapped_column(Float, nullable=False)
    height_delta_percent: Mapped[PositiveFloat] = mapped_column(Float, nullable=False)
    prolixity_index_delta_percent: Mapped[PositiveFloat] = mapped_column(Float, nullable=False)

    def to_schema(self) -> StandardSchema:
        return StandardSchema(
            id=ID(self.id),
            breed_id=ID(self.breed_id),
            country=Country(self.country),
            weight=Weight(self.weight),
            height=Height(self.height),
            has_defects=self.has_defects,
            is_multi_color=self.is_multi_color,
            prolixity_index=ProlixityIndex(self.prolixity_index),
            weight_delta_percent=Weight(self.weight_delta_percent),
            height_delta_percent=Height(self.height_delta_percent),
            prolixity_index_delta_percent=ProlixityIndex(self.prolixity_index_delta_percent)
        )
