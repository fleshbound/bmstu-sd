import enum

from pydantic import BaseModel

from utils.types import ID, AnimalName, Sex, Datetime, ProlixityIndex, Length, Height, Weight


class AnimalSchema(BaseModel):
    id: ID
    user_id: ID
    breed_id: ID
    name: AnimalName
    birth_dt: Datetime
    sex: Sex
    prolixity_index: ProlixityIndex
    weight: Weight
    height: Height
    length: Length
    has_defects: bool
    is_multicolor: bool
    is_archived: bool


class AnimalSchemaCreate(BaseModel):
    user_id: ID
    breed_id: ID
    name: AnimalName
    birth_dt: Datetime
    sex: Sex
    prolixity_index: ProlixityIndex
    weight: Weight
    height: Height
    length: Length
    has_defects: bool
    is_multicolor: bool
    is_archived: bool = False


class AnimalSchemaUpdate(BaseModel):
    id: ID = 0
    name: AnimalName
    birth_dt: Datetime
    sex: Sex
    prolixity_index: ProlixityIndex
    weight: Weight
    height: Height
    length: Length
    has_defects: bool
    is_multicolor: bool


class AnimalSchemaUpdateBody(BaseModel):
    name: AnimalName
    birth_dt: Datetime
    sex: Sex
    prolixity_index: ProlixityIndex
    weight: Weight
    height: Height
    length: Length
    has_defects: bool
    is_multicolor: bool
