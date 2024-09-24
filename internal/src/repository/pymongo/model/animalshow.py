from pydantic import BaseModel, Field

from core.show.schema.animalshow import AnimalShowSchema
from core.utils.types import ID
from repository.utils.types import PyObjectId, int_from_pyobject_id


class AnimalShowODM(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    animal_id: int
    show_id: int
    is_archived: bool

    def to_schema(self) -> AnimalShowSchema:
        return AnimalShowSchema(
            id=ID(int_from_pyobject_id(self.id)),
            animal_id=ID(self.animal_id),
            show_id=ID(self.show_id),
            is_archived=self.is_archived
        )
