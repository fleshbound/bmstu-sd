import datetime

from core.animal.schema.animal import AnimalSchema
from core.utils.types import Weight, Sex, ID, Length, Height, Datetime, AnimalName


class AnimalSchemaBuilder:
    _id: int
    _user_id: int
    _breed_id: int
    _name: str
    _birth_dt: datetime.datetime
    _sex: str
    _weight: float
    _height: float
    _length: float
    _has_defects: bool
    _is_multicolor: bool

    TEST_ANIMAL_ID: int = 1
    TEST_USER_ID: int = 1
    TEST_BREED_ID: int = 1
    TEST_NAME: str = 'Cool Animal Name'
    TEST_BIRTH_DT: datetime.datetime = datetime.datetime(2003, 6, 10)
    TEST_SEX: str = 'female'
    TEST_WEIGHT: float = 100
    TEST_HEIGHT: float = 100
    TEST_LENGTH: float = 100
    TEST_HAS_DEFECTS: bool = False
    TEST_IS_MULTICOLOR: bool = True

    def build(self) -> AnimalSchema:
        return AnimalSchema(
            id=ID(self._id),
            user_id=ID(self._user_id),
            breed_id=ID(self._breed_id),
            name=AnimalName(self._name),
            birth_dt=Datetime(self._birth_dt),
            sex=Sex(self._sex),
            weight=Weight(self._weight),
            height=Height(self._height),
            length=Length(self._length),
            has_defects=self._has_defects,
            is_multicolor=self._is_multicolor
        )

    def with_id(self, id: int):
        self._id = id
        return self

    def with_user_id(self, user_id: int):
        self._user_id = user_id
        return self

    def with_breed_id(self, breed_id: int):
        self._breed_id = breed_id
        return self

    def with_name(self, name: str):
        self._name = name
        return self

    def with_birth_dt(self, birth_dt: datetime.datetime):
        self._birth_dt = birth_dt
        return self

    def with_sex(self, sex: str):
        self._sex = sex
        return self

    def with_height(self, height: float):
        self._height = height
        return self

    def with_weight(self, weight: float):
        self._weight = weight
        return self

    def with_length(self, length: float):
        self._length = length
        return self

    def with_is_multicolor(self, is_multicolor: bool):
        self._is_multicolor = is_multicolor
        return self

    def with_has_defects(self, has_defects: bool):
        self._has_defects = has_defects
        return self

    def from_object(self, object: AnimalSchema):
        self._id = object.id.value
        self._user_id = object.user_id.value
        self._breed_id = object.breed_id.value
        self._name = object.name.value
        self._birth_dt = object.birth_dt.value
        self._sex = object.sex.value
        self._weight = object.weight.value
        self._height = object.height.value
        self._length = object.length.value
        self._has_defects = object.has_defects
        self._is_multicolor = object.is_multicolor
        return self

    def with_test_values(self):
        self._id = self.TEST_ANIMAL_ID
        self._user_id = self.TEST_USER_ID
        self._breed_id = self.TEST_BREED_ID
        self._name = self.TEST_NAME
        self._birth_dt = self.TEST_BIRTH_DT
        self._sex = self.TEST_SEX
        self._weight = self.TEST_WEIGHT
        self._height = self.TEST_HEIGHT
        self._length = self.TEST_LENGTH
        self._has_defects = self.TEST_HAS_DEFECTS
        self._is_multicolor = self.TEST_IS_MULTICOLOR
        return self
