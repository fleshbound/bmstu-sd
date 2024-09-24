from pydantic import NonNegativeInt, NonNegativeFloat, PositiveFloat, BaseModel, Field
from sqlalchemy import ForeignKey, String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from core.standard.schema.standard import StandardSchema
from core.utils.types import ID, Height, Weight, Country, Length
from repository.sqlalchemy.model.base import Base
from repository.utils.types import PyObjectId, int_from_pyobject_id


class StandardORM(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    breed_id: int
    country: str
    weight: float
    height: float
    has_defects: bool
    is_multicolor: bool
    length: float
    weight_delta_percent: float
    height_delta_percent: float
    length_delta_percent: float

    def to_schema(self) -> StandardSchema:
        return StandardSchema(
            id=ID(int_from_pyobject_id(self.id)),
            breed_id=ID(self.breed_id),
            country=Country(self.country),
            weight=Weight(self.weight),
            height=Height(self.height),
            has_defects=self.has_defects,
            is_multicolor=self.is_multicolor,
            length=Length(self.length),
            weight_delta_percent=self.weight_delta_percent,
            height_delta_percent=self.height_delta_percent,
            length_delta_percent=self.length_delta_percent
        )
