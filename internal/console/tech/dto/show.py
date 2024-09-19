from typing import Optional

from pydantic import BaseModel

from console.tech.handler.input import InputHandler
from console.tech.utils.exceptions import CancelInput, InvalidBooleanInput
from console.tech.utils.lang.langmodel import LanguageModel
from core.show.schema.show import ShowSchemaCreate, ShowSchema, ShowClass, ShowStatus
from core.utils.types import ID, ShowName, Country


class ShowDTO(BaseModel):
    id: int
    species_id: Optional[int]
    breed_id: Optional[int]
    status: str
    country: str
    show_class: str
    name: str
    standard_id: Optional[int]
    is_multi_breed: bool
    input_handler: InputHandler
    lm: LanguageModel

    def print(self):
        print("_______________________")
        print(f"{self.lm.out_id}:  {self.id}")
        print(f"{self.lm.out_name}: {self.name}")
        print(f"{self.lm.out_status}: {self.status}")
        print(f"{self.lm.out_show_class}: {self.show_class}")
        print(f"{self.lm.out_country}: {self.country}")
        print(f"{self.lm.out_is_multi_breed}: {self.lm.yes if self.is_multi_breed else self.lm.no}")
        print(f"{self.lm.out_breed_id}: {'-' if self.breed_id is None else self.breed_id}")
        print(f"{self.lm.out_standard_id}: {'-' if self.standard_id is None else self.standard_id}")
        print(f"{self.lm.out_species_id}: {'-' if self.species_id is None else self.species_id}")

    def input_id(self):
        id = self.input_handler.wait_positive_int(
            self.lm.question_show_id,
            self.lm.out_show_id
        )
        if id is None:
            print(self.lm.cancel_input)
            raise CancelInput('show id input cancel')
        self.id = id

    def input_delete(self):
        self.input_id()

    def input_create(self):
        self.id = 0
        self.input_name()
        self.input_country()
        self.input_show_class()
        self.input_is_multi_breed()
        if self.is_multi_breed:
            self.input_species_id()
            self.standard_id = None
            self.breed_id = None
        else:
            self.input_breed_id()
            self.input_standard_id()
            self.species_id = None
        self.status = ShowStatus.created
        return self

    def input_breed_id(self):
        breed_id = self.input_handler.wait_positive_int(
            self.lm.question_breed_id,
            self.lm.out_breed_id
        )
        if breed_id is None:
            print(self.lm.cancel_input)
            raise CancelInput('show breed_id input cancel')
        self.breed_id = breed_id

    def input_species_id(self):
        species_id = self.input_handler.wait_positive_int(
            self.lm.question_species_id,
            self.lm.out_species_id
        )
        if species_id is None:
            print(self.lm.cancel_input)
            raise CancelInput('show species_id input cancel')
        self.species_id = species_id

    def input_standard_id(self):
        standard_id = self.input_handler.wait_positive_int(
            self.lm.question_standard_id,
            self.lm.out_standard_id
        )
        if standard_id is None:
            print(self.lm.cancel_input)
            raise CancelInput('show standard_id input cancel')
        self.standard_id = standard_id

    def input_name(self):
        name = self.input_handler.wait_input(
            self.lm.question_name,
            self.lm.out_name
        )
        if name is None:
            print(self.lm.cancel_input)
            raise CancelInput('show name input cancel')
        self.name = name

    def input_status(self):
        status = self.input_handler.wait_input(
            self.lm.question_status,
            self.lm.out_status
        )
        if status is None:
            print(self.lm.cancel_input)
            raise CancelInput('show status input cancel')
        self.status = status
        # TODO: check status

    def input_country(self):
        country = self.input_handler.wait_input(
            self.lm.question_country,
            self.lm.out_country
        )
        if country is None:
            print(self.lm.cancel_input)
            raise CancelInput('show country input cancel')
        self.country = country
        # TODO: check country

    def input_show_class(self):
        show_class = self.input_handler.wait_input(
            self.lm.question_show_class,
            self.lm.out_show_class
        )
        if show_class is None:
            print(self.lm.cancel_input)
            raise CancelInput('show show_class input cancel')
        self.show_class = show_class
        # TODO: chech class

    def input_is_multi_breed(self):
        is_multi_breed = self.input_handler.wait_input(self.lm.question_is_multi_breed,
                                                       self.lm.out_question_is_multi_breed)
        if is_multi_breed is None:
            print(self.lm.cancel_input)
            raise CancelInput('show is_multi_breed input cancel')
        if is_multi_breed.upper() != self.lm.yes.upper() and is_multi_breed.upper() != self.lm.no.upper():
            print(self.lm.cancel_input)
            raise InvalidBooleanInput('is_multi_breed')
        self.is_multi_breed = True if is_multi_breed.upper() == self.lm.yes.upper() else False

    def to_schema_create(self) -> ShowSchemaCreate:
        standard_id = self.standard_id if self.standard_id is None else ID(self.standard_id)
        species_id = self.species_id if self.species_id is None else ID(self.species_id)
        breed_id = self.breed_id if self.breed_id is None else ID(self.breed_id)
        return ShowSchemaCreate(
            species_id=species_id,
            breed_id=breed_id,
            country=Country(self.country),
            show_class=ShowClass(self.show_class),
            name=ShowName(self.name),
            standard_id=standard_id,
            is_multi_breed=self.is_multi_breed
        )

    @classmethod
    def from_schema(cls, other: ShowSchema):
        standard_id = other.standard_id if other.standard_id is None else ID(other.standard_id)
        species_id = other.species_id if other.species_id is None else ID(other.species_id)
        breed_id = other.breed_id if other.breed_id is None else ID(other.breed_id)
        return cls(
            id=other.id.value,
            species_id=species_id,
            breed_id=breed_id,
            country=other.country.value,
            show_class=other.show_class.value,
            status=other.status.value,
            name=other.name.value,
            standard_id=standard_id,
            is_multi_breed=other.is_multi_breed
        )
