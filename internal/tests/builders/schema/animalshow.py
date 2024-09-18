from core.show.schema.animalshow import AnimalShowSchema
from core.utils.types import ID


class AnimalShowSchemaBuilder:
    _id: int
    _animal_id: int
    _show_id: int
    _is_archived: bool

    TEST_ID: int = 1
    TEST_ANIMAL_ID: int = 1
    TEST_SHOW_ID: int = 1
    TEST_IS_ARCHIVED: bool = False

    def build(self):
        return AnimalShowSchema(
            id=ID(self._id),
            animal_id=ID(self._animal_id),
            show_id=ID(self._show_id),
            is_archived=self._is_archived
        )

    def with_id(self, id: int):
        self._id = id
        return self

    def with_animal_id(self, animal_id: int):
        self._animal_id = animal_id
        return self

    def with_show_id(self, show_id: int):
        self._show_id = show_id
        return self

    def with_is_archived(self, is_archived: bool):
        self._is_archived = is_archived
        return self

    def with_test_values(self):
        self._id = self.TEST_ID
        self._show_id = self.TEST_SHOW_ID
        self._animal_id = self.TEST_ANIMAL_ID
        self._is_archived = self.TEST_IS_ARCHIVED
        return self

    def from_object(self, other: AnimalShowSchema):
        self._id = other.id.value
        self._show_id = other.show_id.value
        self._animal_id = other.animal_id.value
        self._is_archived = other.is_archived
        return self
