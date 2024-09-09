from typing import Optional

from internal.src.core.show.schema.show import ShowSchema, ShowClass, ShowStatus
from internal.src.core.utils.types import ID, Country, ShowName


class ShowSchemaBuilder:
    _id: int
    _species_id: Optional[int]
    _breed_id: Optional[int]
    _status: str
    _country: str
    _show_class: str
    _name: str
    _standard_id: Optional[int]
    _is_multi_breed: bool

    TEST_ID: int = 1
    TEST_SPECIES_ID: Optional[int] = None
    TEST_BREED_ID: Optional[int] = 1
    TEST_STATUS: str = 'created'
    TEST_COUNTRY: str = 'Russian Federation'
    TEST_SHOW_CLASS: str = 'one'
    TEST_NAME: str = 'Cool Show Name'
    TEST_STANDARD_ID: Optional[int] = 1
    TEST_IS_MULTI_BREED: bool = False

    def build(self) -> ShowSchema:
        standard_id = self._standard_id if self._standard_id is None else ID(self._standard_id)
        species_id = self._species_id if self._species_id is None else ID(self._species_id)
        breed_id = self._breed_id if self._breed_id is None else ID(self._breed_id)
        return ShowSchema(
            id=ID(self._id),
            status=ShowStatus(self._status),
            name=ShowName(self._name),
            species_id=species_id,
            breed_id=breed_id,
            country=Country(self._country),
            show_class=ShowClass(self._show_class),
            standard_id=standard_id,
            is_multi_breed=self._is_multi_breed
        )

    def with_id(self, id: int):
        self._id = id
        return self

    def with_name(self, name: str):
        self._name = name
        return self

    def with_status(self, status: str):
        self._status = status
        return self

    def with_species_id(self, species_id: Optional[int]):
        self._species_id = species_id
        return self

    def with_breed_id(self, breed_id: Optional[int]):
        self._breed_id = breed_id
        return self

    def with_country(self, country: str):
        self._country = country
        return self

    def with_show_class(self, show_class: str):
        self._show_class = show_class
        return self

    def with_standard_id(self, standard_id: Optional[int]):
        self._standard_id = standard_id
        return self

    def with_is_multi_breed(self, is_multi_breed: bool):
        self._is_multi_breed = is_multi_breed
        return self

    def from_object(self, object: ShowSchema):
        self._id = object.id.value
        self._status = object.status.value
        self._name = object.name.value
        self._species_id = object.species_id.value
        self._breed_id = object.breed_id.value
        self._country = object.country.value
        self._show_class = object.show_class.value
        self._standard_id = object.standard_id.value
        self._is_multi_breed = object.is_multi_breed
        return self

    def with_test_values(self):
        self._id = self.TEST_ID
        self._status = self.TEST_STATUS
        self._name = self.TEST_NAME
        self._species_id = self.TEST_SPECIES_ID
        self._breed_id = self.TEST_BREED_ID
        self._country = self.TEST_COUNTRY
        self._show_class = self.TEST_SHOW_CLASS
        self._standard_id = self.TEST_STANDARD_ID
        self._is_multi_breed = self.TEST_IS_MULTI_BREED
        return self
