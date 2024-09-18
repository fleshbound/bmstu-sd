from core.group.schema.group import GroupSchema
from core.utils.types import ID, GroupName


class GroupSchemaBuilder:
    _id: int
    _name: str

    TEST_ID: int = 1
    TEST_NAME: str = 'Cool Group Name'

    def build(self) -> GroupSchema:
        return GroupSchema(id=ID(self._id), name=GroupName(self._name))

    def with_id(self, id: int):
        self._id = id
        return self

    def with_name(self, name: str):
        self._name = name
        return self

    def with_test_values(self):
        self._id = self.TEST_ID
        self._name = self.TEST_NAME
        return self

    def from_object(self, object: GroupSchema):
        self._id = object.id.value
        self._name = object.name.value
        return self
