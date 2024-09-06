from internal.src.core.species.schema.species import SpeciesSchema
from internal.src.core.utils.types import ID, SpeciesName


class SpeciesSchemaBuilder:
    _id: int
    _name: str
    _group_id: int

    TEST_ID: int = 1
    TEST_NAME: str = 'Cool Species'
    TEST_GROUP_ID: int = 1

    def build(self) -> SpeciesSchema:
        return SpeciesSchema(id=ID(self._id), name=SpeciesName(self._name), group_id=ID(self._group_id))

    def with_id(self, id: int):
        self._id = id
        return self

    def with_group_id(self, group_id: int):
        self._group_id = group_id
        return self

    def with_name(self, name: str):
        self._name = name
        return self

    def with_test_values(self):
        self._id = self.TEST_ID
        self._name = self.TEST_NAME
        self._group_id = self.TEST_GROUP_ID
        return self

    def from_object(self, object: SpeciesSchema):
        self._id = object.id.value
        self._name = object.name.value
        self._group_id = object.group_id.value
        return self
