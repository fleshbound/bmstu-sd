import datetime

from pydantic import BaseModel, Field

from core.animal.schema.animal import AnimalSchema
from repository.utils.types import PyObjectId, int_from_pyobject_id
from utils.types import ID, AnimalName, Datetime, Sex, Height, Weight, Length


class AnimalODM(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    user_id: int
    breed_id: int
    name: str
    birth_dt: datetime.datetime
    sex: str
    weight: float
    height: float
    has_defects: bool
    is_multicolor: bool

    def to_schema(self) -> AnimalSchema:
        return AnimalSchema(
            id=ID(int_from_pyobject_id(self.id)),
            user_id=ID(self.user_id),
            breed_id=ID(self.breed_id),
            name=AnimalName(self.name),
            birth_dt=Datetime(self.birth_dt),
            sex=Sex(self.sex),
            weight=Weight(self.weight),
            height=Height(self.height),
            length=Length(self.length),
            has_defects=self.has_defects,
            is_multicolor=self.is_multicolor
        )
