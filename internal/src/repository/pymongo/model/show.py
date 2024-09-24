from pydantic import BaseModel, Field

from core.show.schema.show import ShowSchema, ShowStatus, ShowClass
from core.utils.types import ID, ShowName, Country
from repository.utils.types import PyObjectId, int_from_pyobject_id


class ShowORM(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    species_id: int
    standard_id: int
    breed_id: int
    status: str
    country: str
    show_class: str
    name: str
    is_multi_breed: bool

    def to_schema(self) -> ShowSchema:
        standard_id = self.standard_id if self.standard_id is None else ID(self.standard_id)
        species_id = self.species_id if self.species_id is None else ID(self.species_id)
        breed_id = self.breed_id if self.breed_id is None else ID(self.breed_id)
        return ShowSchema(
            id=ID(int_from_pyobject_id(self.id)),
            species_id=species_id,
            breed_id=breed_id,
            country=Country(self.country),
            status=ShowStatus(self.status),
            show_class=ShowClass(self.show_class),
            standard_id=standard_id,
            name=ShowName(self.name),
            is_multi_breed=self.is_multi_breed
        )
