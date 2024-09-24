from pydantic import BaseModel, Field

from core.species.schema.species import SpeciesSchema
from core.utils.types import ID, SpeciesName
from repository.utils.types import PyObjectId, int_from_pyobject_id


class SpeciesORM(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    group_id: int
    name: str

    def to_schema(self) -> SpeciesSchema:
        return SpeciesSchema(
            id=ID(int_from_pyobject_id(self.id)),
            group_id=ID(self.group_id),
            name=SpeciesName(self.name)
        )
