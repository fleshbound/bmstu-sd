from core.standard.schema.standard import StandardSchema
from core.utils.types import Weight, ID, Length, Height, Country


class StandardSchemaBuilder:
    _id: int
    _country: str
    _breed_id: int
    _weight: float
    _height: float
    _length: float
    _weight_delta_percent: float
    _height_delta_percent: float
    _length_delta_percent: float
    _has_defects: bool
    _is_multicolor: bool

    TEST_ANIMAL_ID: int = 1
    TEST_COUNTRY: str = 'Russian Federation'
    TEST_BREED_ID: int = 1
    TEST_WEIGHT: float = 100
    TEST_HEIGHT: float = 100
    TEST_LENGTH: float = 100
    TEST_WEIGHT_DELTA_PERCENT: float = 10
    TEST_HEIGHT_DELTA_PERCENT: float = 10
    TEST_LENGTH_DELTA_PERCENT: float = 10
    TEST_HAS_DEFECTS: bool = False
    TEST_IS_MULTICOLOR: bool = True

    def build(self) -> StandardSchema:
        return StandardSchema(
            id=ID(self._id),
            breed_id=ID(self._breed_id),
            country=Country(self._country),
            weight=Weight(self._weight),
            height=Height(self._height),
            length=Length(self._length),
            weight_delta_percent=self._weight_delta_percent,
            height_delta_percent=self._height_delta_percent,
            length_delta_percent=self._length_delta_percent,
            has_defects=self._has_defects,
            is_multicolor=self._is_multicolor
        )

    def with_id(self, id: int):
        self._id = id
        return self

    def with_breed_id(self, breed_id: int):
        self._breed_id = breed_id
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

    def with_country(self, country: str):
        self._country = country
        return self

    def with_height_delta_percent(self, height_delta_percent: float):
        self._height_delta_percent = height_delta_percent
        return self

    def with_weight_delta_percent(self, weight_delta_percent: float):
        self._weight_delta_percent = weight_delta_percent
        return self

    def with_length_delta_percent(self, length_delta_percent: float):
        self._length_delta_percent = length_delta_percent
        return self

    def with_is_multicolor(self, is_multicolor: bool):
        self._is_multicolor = is_multicolor
        return self

    def with_has_defects(self, has_defects: bool):
        self._has_defects = has_defects
        return self

    def from_object(self, object: StandardSchema):
        self._id = object.id.value
        self._breed_id = object.breed_id.value
        self._weight = object.weight.value
        self._country = object.country.value
        self._height = object.height.value
        self._length = object.length.value
        self._weight_delta_percent = object.weight.value
        self._height_delta_percent = object.height.value
        self._length_delta_percent = object.length.value
        self._has_defects = object.has_defects
        self._is_multicolor = object.is_multicolor
        return self

    def with_test_values(self):
        self._id = self.TEST_ANIMAL_ID
        self._breed_id = self.TEST_BREED_ID
        self._weight = self.TEST_WEIGHT
        self._country = self.TEST_COUNTRY
        self._height = self.TEST_HEIGHT
        self._length = self.TEST_LENGTH
        self._weight_delta_percent = self.TEST_WEIGHT_DELTA_PERCENT
        self._height_delta_percent = self.TEST_HEIGHT_DELTA_PERCENT
        self._length_delta_percent = self.TEST_LENGTH_DELTA_PERCENT
        self._has_defects = self.TEST_HAS_DEFECTS
        self._is_multicolor = self.TEST_IS_MULTICOLOR
        return self
