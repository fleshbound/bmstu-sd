import enum

from pydantic import BaseModel

from core.utils.types import ID, BreedName


class BreedSchema(BaseModel):
    id: ID
    species_id: ID
    name: BreedName


class BreedSchemaUpdate(BaseModel):
    id: ID
    name: BreedName


class BreedSchemaCreate(BaseModel):
    species_id: ID
    name: BreedName


class BreedDeleteStatus(str, enum.Enum):
    deleted = "deleted"


class BreedSchemaDelete(BaseModel):
    id: ID
    status: BreedDeleteStatus = BreedDeleteStatus.deleted
