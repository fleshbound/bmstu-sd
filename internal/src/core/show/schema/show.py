import enum
from typing import List, Optional

from pydantic import BaseModel, NonNegativeInt

from core.animal.schema.animal import AnimalSchema
from core.show.schema.score import AniShowRankingInfo
from core.user.schema.user import UserSchema
from core.utils.types import Country, ShowName, ID


@enum.unique
class ShowClass(str, enum.Enum):
    one = "one"
    two = "two"
    three = "three"


@enum.unique
class ShowStatus(str, enum.Enum):
    created = "created"
    started = "started"
    stopped = "stopped"
    aborted = "aborted"


class ShowSchemaCreate(BaseModel):
    species_id: Optional[ID]
    breed_id: Optional[ID]
    status: ShowStatus
    country: Country
    s_class: ShowClass
    name: ShowName
    standard_id: Optional[ID]
    is_multi_breed: bool


class ShowSchemaUpdate(BaseModel):
    id: ID
    status: ShowStatus
    name: ShowName
    

class ShowSchema(BaseModel):
    id: ID
    species_id: Optional[ID]
    breed_id: Optional[ID]
    status: ShowStatus
    country: Country
    show_class: ShowClass
    name: ShowName
    standard_id: Optional[ID]
    is_multi_breed: bool

    @classmethod
    def from_create(cls, create: ShowSchemaCreate):
        return cls(
            id=ID(0),
            status=create.status,
            name=create.name,
            species_id=create.species_id,
            breed_id=create.breed_id,
            country=create.country,
            show_class=create.show_class,
            standard_id=create.standard_id,
            is_multi_breed=create.is_multi_breed
        )

    def from_update(self, update: ShowSchemaUpdate):
        return ShowSchema(
            id=self.id,
            status=update.status,
            name=update.name,
            species_id=self.species_id,
            breed_id=self.breed_id,
            country=self.country,
            show_class=self.show_class,
            standard_id=self.standard_id,
            is_multi_breed=self.is_multibreed
        )


class ShowSchemaDetailed(BaseModel):
    id: ID
    species_id: Optional[ID]
    breed_id: Optional[ID]
    status: ShowStatus
    country: Country
    show_class: ShowClass
    name: ShowName
    standard_id: Optional[ID]
    is_multi_breed: bool
    animals: List[AnimalSchema]
    users: List[UserSchema]

    @classmethod
    def from_schema(cls, other: ShowSchema):
        return cls(
            id=other.id,
            status=other.status,
            name=other.name,
            species_id=other.species_id,
            breed_id=other.breed_id,
            country=other.country,
            show_class=other.show_class,
            is_multi_breed=other.is_multi_breed,
            standard_id=other.standard_id,
            animals=[],
            users=[]
        )


class ShowSchemaReport(BaseModel):
    ranking_info: List[AniShowRankingInfo]
    rank_count: NonNegativeInt


class ShowSchemaUpdateBody(BaseModel):
    status: ShowStatus
    name: ShowName


class ShowSchemaAbort(BaseModel):
    id: ID
    species_id: Optional[ID]
    breed_id: Optional[ID]
    status: ShowStatus
    country: Country
    standard_id: Optional[ID]
    show_class: ShowClass
    name: ShowName
    is_multi_breed: bool


@enum.unique
class ShowRegisterAnimalStatus(str, enum.Enum):
    register_ok = "ok"
    register_error = "error"
    unregister_ok = "unregok"
    unregister_error = "unregerror"


class ShowRegisterAnimalResult(BaseModel):
    record_id: Optional[ID]
    status: ShowRegisterAnimalStatus


@enum.unique
class ShowRegisterUserStatus(str, enum.Enum):
    register_ok = "regok"
    register_error = "regerror"
    unregister_ok = "unregok"
    unregister_error = "unregerror"


class ShowRegisterUserResult(BaseModel):
    record_id: Optional[ID]
    status: ShowRegisterUserStatus
