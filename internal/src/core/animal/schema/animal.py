from pydantic import BaseModel

from core.utils.types import ID, AnimalName, Sex, Datetime, Length, Height, Weight


class AnimalSchemaCreate(BaseModel):
    user_id: ID
    breed_id: ID
    name: AnimalName
    birth_dt: Datetime
    sex: Sex
    weight: Weight
    height: Height
    length: Length
    has_defects: bool
    is_multicolor: bool
    is_archived: bool = False


class AnimalSchemaUpdate(BaseModel):
    id: ID
    name: AnimalName
    birth_dt: Datetime
    weight: Weight
    height: Height
    length: Length
    has_defects: bool
    is_multicolor: bool


class AnimalSchema(BaseModel):
    id: ID
    user_id: ID
    breed_id: ID
    name: AnimalName
    birth_dt: Datetime
    sex: Sex
    weight: Weight
    height: Height
    length: Length
    has_defects: bool
    is_multicolor: bool
    is_archived: bool

    @classmethod
    def from_create(cls, other: AnimalSchemaCreate):
        return cls(
            id=ID(0),
            user_id=other.user_id,
            breed_id=other.breed_id,
            name=other.name,
            birth_dt=other.birth_dt,
            sex=other.sex,
            weight=other.weight,
            height=other.height,
            length=other.length,
            has_defects=other.has_defects,
            is_multicolor=other.is_multicolor,
            is_archived=False
        )

    def from_update(self, other: AnimalSchemaUpdate):
        return AnimalSchema(
            id=other.id,
            user_id=self.user_id,
            breed_id=self.breed_id,
            name=other.name,
            birth_dt=other.birth_dt,
            sex=self.sex,
            weight=other.weight,
            height=other.height,
            length=other.length,
            has_defects=other.has_defects,
            is_multicolor=other.is_multicolor,
            is_archived=self.is_archived
        )

class AnimalSchemaDelete(BaseModel):
    id: ID
    status: str = 'deleted'
