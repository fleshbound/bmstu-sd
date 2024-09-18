import datetime

from core.show.schema.score import ScoreSchema
from core.utils.types import ID, ScoreValue, Datetime


class ScoreSchemaBuilder:
    _id: int
    _animalshow_id: int
    _usershow_id: int
    _value: int
    _dt_created: datetime.datetime
    _is_archived: bool

    TEST_ID: int = 1
    TEST_ANIMALSHOW_ID: int = 1
    TEST_USERSHOW_ID: int = 1
    TEST_VALUE: int = 4
    TEST_DT_CREATED: datetime.datetime = datetime.datetime(2020, 10, 5)
    TEST_IS_ARCHIVED: bool = False

    def build(self) -> ScoreSchema:
        return ScoreSchema(
            id=ID(self._id),
            animalshow_id=ID(self._animalshow_id),
            usershow_id=ID(self._usershow_id),
            value=ScoreValue(self._value),
            dt_created=Datetime(self._dt_created),
            is_archived=self._is_archived
        )

    def with_id(self, id: int):
        self._id = id
        return self

    def with_animalshow_id(self, animalshow_id: int):
        self._animalshow_id = animalshow_id
        return self

    def with_usershow_id(self, usershow_id: int):
        self._usershow_id = usershow_id
        return self

    def with_value(self, value: int):
        self._value = value
        return self

    def with_is_archived(self, is_archived: bool):
        self._is_archived = is_archived
        return self

    def with_dt_created(self, dt_created: datetime.datetime):
        self._dt_created = dt_created
        return self

    def with_test_values(self):
        self._id = self.TEST_ID
        self._animalshow_id = self.TEST_ANIMALSHOW_ID
        self._usershow_id = self.TEST_USERSHOW_ID
        self._value = self.TEST_VALUE
        self._dt_created = self.TEST_DT_CREATED
        self._is_archived = self.TEST_IS_ARCHIVED
        return self

    def from_object(self, other: ScoreSchema):
        self._id = other.id.value
        self._animalshow_id = other.animalshow_id.value
        self._usershow_id = other.usershow_id.value
        self._value = other.value.value
        self._dt_created = other.dt_created.value
        self._is_archived = other.is_archived
        return self
