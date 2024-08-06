import enum
from typing import List, Optional

from pydantic import BaseModel

from core.animal.schema.animal import AnimalSchema
from core.user.schema.user import UserSchema
from utils.types import Country, ShowName, ID


@enum.unique
class ShowState(str, enum.Enum):
    open = "open"
    started = "started"
    closed = "closed"
    aborted = "aborted"


@enum.unique
class ShowClass(str, enum.Enum):
    one = "one"
    two = "two"
    three = "three"


class ShowSchema(BaseModel):
    id: ID
    species_id: Optional[ID]
    breed_id: Optional[ID]
    state: ShowState
    country: Country
    show_class: ShowClass
    name: ShowName
    is_multi_breed: bool


class ShowSchemaDetailed(BaseModel):
    id: ID
    species_id: Optional[ID]
    breed_id: Optional[ID]
    state: ShowState
    country: Country
    show_class: ShowClass
    name: ShowName
    is_multi_breed: bool
    animals: List[AnimalSchema]
    users: List[UserSchema]


class ShowSchemaCreate(BaseModel):
    species_id: Optional[ID]
    breed_id: Optional[ID]
    state: ShowState
    country: Country
    s_class: ShowClass
    name: ShowName
    is_multi_breed: bool


class ShowSchemaUpdate(BaseModel):
    state: ShowState
    name: ShowName


class ShowSchemaUpdateBody(BaseModel):
    state: ShowState
    name: ShowName


class ShowSchemaAbort(BaseModel):
    id: ID
    species_id: Optional[ID]
    breed_id: Optional[ID]
    state: ShowState
    country: Country
    show_class: ShowClass
    name: ShowName
    is_multi_breed: bool


class ShowRegisterAnimalStatus(str, enum.Enum):
    register_ok = "ok"
    register_error = "error"


class ShowRegisterAnimalResult(BaseModel):
    record_id: Optional[ID]
    status: ShowRegisterAnimalStatus
