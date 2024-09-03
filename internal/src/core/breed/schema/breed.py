import enum

from pydantic import BaseModel

from internal.src.core.utils.types import ID, BreedName


class BreedSchemaUpdate(BaseModel):
    id: ID
    name: BreedName


class BreedSchemaCreate(BaseModel):
    species_id: ID
    name: BreedName


class BreedSchema(BaseModel):
    id: ID
    species_id: ID
    name: BreedName

    @classmethod
    def from_create(cls, other: BreedSchemaCreate):
        return cls(
            id=ID(0),
            species_id=other.species_id,
            name=other.name
        )

    def from_update(self, other: BreedSchemaUpdate):
        return BreedSchemaUpdate(
            id=other.id,
            species_id=self.species_id,
            name=other.name
        )


class BreedDeleteStatus(str, enum.Enum):
    deleted = "deleted"


class BreedSchemaDelete(BaseModel):
    id: ID
    status: BreedDeleteStatus = BreedDeleteStatus.deleted
