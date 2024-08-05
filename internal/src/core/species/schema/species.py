import enum

from pydantic import BaseModel

from utils.types import SpeciesName, ID


class SpeciesSchema(BaseModel):
    id: ID
    group_id: ID
    name: SpeciesName


class SpeciesSchemaUpdate(BaseModel):
    id: ID
    name: SpeciesName


class SpeciesSchemaCreate(BaseModel):
    group_id: ID
    name: SpeciesName
    

class SpeciesDeleteStatus(str, enum.Enum):
    deleted = "deleted"


class SpeciesSchemaDelete(BaseModel):
    id: ID
    status: SpeciesDeleteStatus = SpeciesDeleteStatus.deleted
