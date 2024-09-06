from internal.src.core.breed.schema.breed import BreedSchema
from internal.src.core.utils.types import ID, BreedName


class BreedSchemaBuilder:
    _id: int
    _name: str
    _species_id: int

    TEST_ID: int = 1
    TEST_NAME: str = 'Cool Breed'
    TEST_SPECIES_ID: int = 1

    def build(self) -> BreedSchema:
        return BreedSchema(id=ID(self._id), name=BreedName(self._name), species_id=ID(self._species_id))

    def with_id(self, id: int):
        self._id = id
        return self

    def with_species_id(self, species_id: int):
        self._species_id = species_id
        return self

    def with_name(self, name: str):
        self._name = name
        return self

    def with_test_values(self):
        self._id = self.TEST_ID
        self._name = self.TEST_NAME
        self._species_id = self.TEST_SPECIES_ID
        return self

    def from_object(self, object: BreedSchema):
        self._id = object.id.value
        self._name = object.name.value
        self._species_id = object.species_id.value
        return self
