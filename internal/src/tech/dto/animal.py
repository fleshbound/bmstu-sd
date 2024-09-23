import datetime

from pydantic import BaseModel

from tech.handlers.input import InputHandler
from tech.utils.exceptions import CancelInput, InvalidFloatInput, InvalidSexInput, InvalidBooleanInput
from tech.utils.lang.langmodel import LanguageModel
from core.animal.schema.animal import AnimalSchemaCreate, AnimalSchema
from core.utils.types import Sex, ID, AnimalName, Datetime, Weight, Height, Length


class AnimalDTO:
    id: int
    user_id: int
    breed_id: int
    name: str
    birth_dt: datetime.datetime
    sex: str
    weight: float
    height: float
    length: float
    has_defects: bool
    is_multicolor: bool
    input_handler: InputHandler
    lm: LanguageModel

    def print(self):
        print("_______________________")
        print(f"{self.lm.out_id}:  {self.id}")
        print(f"{self.lm.out_name}: {self.name}")
        print(f"{self.lm.out_breed_id}: {self.breed_id}")
        print(f"{self.lm.out_user_id}: {self.user_id}")
        print(f"{self.lm.out_birth_dt}: {str(self.birth_dt.date())}")
        print(f"{self.lm.out_sex}: {self.lm.out_sex_male if self.sex == Sex.male else self.lm.out_sex_female}")
        print(f"{self.lm.out_weight}: {self.weight:5.3f} {self.lm.out_weight_unit}")
        print(f"{self.lm.out_height}: {self.height:5.1f} {self.lm.out_height_unit}")
        print(f"{self.lm.out_length}: {self.length:5.1f} {self.lm.out_length_unit}")
        print(f"{self.lm.out_has_defects}: {self.lm.yes if self.has_defects else self.lm.no}")
        print(f"{self.lm.out_is_multicolor}: {self.lm.yes if self.is_multicolor else self.lm.no}")

    def input_id(self):
        id = self.input_handler.wait_positive_int(
            self.lm.question_animal_id,
            self.lm.out_animal_id
        )
        if id is None:
            print(self.lm.cancel_input)
            raise CancelInput('animal id input cancel')
        self.id = id

    def input_delete(self):
        self.input_id()

    def input_create(self, user_id: int):
        self.id = 0
        self.input_name()
        self.input_breed_id()
        self.input_sex()
        self.input_birth_dt()
        self.input_weight()
        self.input_height()
        self.input_length()
        self.input_has_defects()
        self.input_is_multicolor()
        self.with_user_id(user_id)

    def input_birth_dt(self):
        birth_dt = self.input_handler.date_input(
            self.lm.out_birth_dt
        )
        if birth_dt is None:
            print(self.lm.cancel_input)
            raise CancelInput('animal birth_dt input cancel')
        self.birth_dt = birth_dt

    def with_user_id(self, user_id: int):
        self.user_id = user_id

    def input_breed_id(self):
        breed_id = self.input_handler.wait_positive_int(
            self.lm.question_breed_id,
            self.lm.out_breed_id
        )
        if breed_id is None:
            print(self.lm.cancel_input)
            raise CancelInput('animal breed_id input cancel')
        self.breed_id = breed_id

    def input_name(self):
        name = self.input_handler.wait_input(
            self.lm.question_name,
            self.lm.out_name
        )
        if name is None:
            print(self.lm.cancel_input)
            raise CancelInput('animal name input cancel')
        self.name = name

    def input_weight(self):
        weight = self.input_handler.wait_input(
            self.lm.question_weight,
            self.lm.out_weight
        )
        if weight is None:
            print(self.lm.cancel_input)
            raise CancelInput('animal weight input cancel')
        try:
            self.weight = float(weight)
        except ValueError:
            raise InvalidFloatInput('weight')

    def input_length(self):
        length = self.input_handler.wait_input(
            self.lm.question_length,
            self.lm.out_length
        )
        if length is None:
            print(self.lm.cancel_input)
            raise CancelInput('animal length input cancel')
        try:
            self.length = float(length)
        except ValueError:
            raise InvalidFloatInput('length')

    def input_height(self):
        height = self.input_handler.wait_input(
            self.lm.question_height,
            self.lm.out_height
        )
        if height is None:
            print(self.lm.cancel_input)
            raise CancelInput('animal height input cancel')
        try:
            self.height = float(height)
        except ValueError:
            raise InvalidFloatInput('height')

    def input_sex(self):
        sex = self.input_handler.wait_input(
            self.lm.question_sex,
            self.lm.out_sex
        )
        if sex is None:
            print(self.lm.cancel_input)
            raise CancelInput('animal sex input cancel')
        if (sex.upper() != self.lm.out_sex_male.upper() and sex.upper() != self.lm.out_sex_male_short.upper() and
            sex.upper() != self.lm.out_sex_female.upper() and sex.upper() != self.lm.out_sex_female_short.upper()):
            raise InvalidSexInput()
        self.sex = sex

    def input_has_defects(self):
        has_defects = self.input_handler.wait_input(self.lm.question_has_defects,
                                                    self.lm.out_question_has_defects)
        if has_defects is None:
            print(self.lm.cancel_input)
            raise CancelInput('animal has_defects input cancel')
        if has_defects.upper() != self.lm.yes.upper() and has_defects.upper() != self.lm.no.upper():
            print(self.lm.cancel_input)
            raise InvalidBooleanInput('has_defects')
        self.has_defects = True if has_defects.upper() == self.lm.yes.upper() else False

    def input_is_multicolor(self):
        is_multicolor = self.input_handler.wait_input(self.lm.question_is_multicolor,
                                                      self.lm.out_question_is_multicolor)
        if is_multicolor is None:
            print(self.lm.cancel_input)
            raise CancelInput('animal is_multicolor input cancel')
        if is_multicolor.upper() != self.lm.yes.upper() and is_multicolor.upper() != self.lm.no.upper():
            print(self.lm.cancel_input)
            raise InvalidBooleanInput('is_multicolor')
        self.is_multicolor = True if is_multicolor.upper() == self.lm.yes.upper() else False

    def to_schema_create(self) -> AnimalSchemaCreate:
        return AnimalSchemaCreate(
            user_id=ID(self.user_id),
            breed_id=ID(self.breed_id),
            name=AnimalName(self.name),
            birth_dt=Datetime(self.birth_dt),
            sex=Sex(self.sex),
            weight=Weight(self.weight),
            height=Height(self.height),
            length=Length(self.length),
            has_defects=self.has_defects,
            is_multicolor=self.is_multicolor
        )

    @classmethod
    def from_schema(cls, other: AnimalSchema, input_handler: InputHandler):
        return cls(
            id=other.id.value,
            user_id=other.user_id.value,
            breed_id=other.breed_id.value,
            name=other.name.value,
            birth_dt=other.birth_dt.value,
            sex=other.sex,
            weight=other.weight.value,
            height=other.height.value,
            length=other.length.value,
            has_defects=other.has_defects,
            is_multicolor=other.is_multicolor,
            input_handler=input_handler,
            lm=input_handler.lang_model
        )
