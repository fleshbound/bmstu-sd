from pydantic import Field, BaseModel

from core.breed.schema.breed import BreedSchema
from core.utils.types import ID, BreedName
from repository.utils.types import PyObjectId, int_from_pyobject_id


class BreedORM(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    species_id: int
    name: str

    def to_schema(self) -> BreedSchema:
        return BreedSchema(
            id=ID(int_from_pyobject_id(self.id)),
            species_id=ID(self.species_id),
            name=BreedName(self.name)
        )
