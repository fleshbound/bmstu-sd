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
            is_multicolor=other.is_multicolor
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
            is_multicolor=other.is_multicolor
        )
    
    def __eq__(self, other):
        cond = (self.id == other.id
                and self.user_id == other.user_id
                and self.breed_id == other.breed_id
                and self.weight == other.weight
                and self.length == other.length
                and self.height == other.height
                and self.has_defects == other.has_defects
                and self.is_multicolor == other.is_multicolor
                and self.name == other.name
                and self.sex == other.sex)
        return cond


class AnimalSchemaDelete(BaseModel):
    id: ID
    status: str = 'deleted'
