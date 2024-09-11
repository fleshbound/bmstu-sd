import datetime

from pydantic import BaseModel

from internal.console.tech.handler.input import InputHandler
from internal.console.tech.utils.exceptions import CancelInput
from internal.console.tech.utils.lang.langmodel import LanguageModel
from internal.src.core.utils.types import Sex


class AnimalDTO(BaseModel):
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

    def input_birth_dt(self):
        birth_dt = self.input_handler.wait_positive_int(
            self.input_handler.lang_model.question_animal_birth_dt,
            self.input_handler.lang_model.out_question_animal_birth_dt
        )
        if birth_dt is None:
            print(self.input_handler.lang_model.cancel_input)
            raise CancelInput('animal birth_dt input cancel')
        self.birth_dt = birth_dt

    def input_breed_id(self):
        breed_id = self.input_handler.wait_positive_int(
            self.input_handler.lang_model.question_animal_breed_id,
            self.input_handler.lang_model.out_question_animal_breed_id
        )
        if breed_id is None:
            print(self.input_handler.lang_model.cancel_input)
            raise CancelInput('animal breed_id input cancel')
        self.breed_id = breed_id

    def input_name(self):
        name = self.input_handler.wait_input(
            self.input_handler.lang_model.question_input_animal_name,
            self.input_handler.lang_model.out_question_animal_name
        )
        if name is None:
            print(self.input_handler.lang_model.cancel_input)
            raise CancelInput('animal name input cancel')
        self.name = name

    def input_create(self):
        pass




