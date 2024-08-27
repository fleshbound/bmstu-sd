import enum

from pydantic import BaseModel

from core.utils.types import SpeciesName, ID


class SpeciesSchemaUpdate(BaseModel):
    id: ID
    name: SpeciesName


class SpeciesSchemaCreate(BaseModel):
    group_id: ID
    name: SpeciesName


class SpeciesSchema(BaseModel):
    id: ID
    group_id: ID
    name: SpeciesName

    @classmethod
    def from_create(cls, other: SpeciesSchemaCreate):
        return cls(
            id=ID(0),
            group_id=other.group_id,
            name=other.name
        )

    def from_update(self, other: SpeciesSchemaUpdate):
        return SpeciesSchema(
            id=other.id,
            group_id=self.group_id,
            name=other.name
        )
    

class SpeciesDeleteStatus(str, enum.Enum):
    deleted = "deleted"


class SpeciesSchemaDelete(BaseModel):
    id: ID
    status: SpeciesDeleteStatus = SpeciesDeleteStatus.deleted
