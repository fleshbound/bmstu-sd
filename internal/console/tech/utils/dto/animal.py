import datetime

from internal.console.tech.input import InputHandler
from internal.console.tech.utils.exceptions import CancelInput
from internal.src.core.utils.types import Sex


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

    def print(self):
        print("_______________________")
        print(f"ID:  {self.id}")
        print(f"Имя: {self.name}")
        print(f"ID породы: {self.breed_id}")
        print(f"ID пользователя: {self.user_id}")
        print(f"Дата рождения: {str(self.birth_dt.date())} (гггг.мм.дд)")
        print(f"Пол: {'мужской' if self.sex == Sex.male else 'женский'}")
        print(f"Вес: {self.weight:5.3f} кг")
        print(f"Высота: {self.height:5.1f} см")
        print(f"Длина: {self.length:5.1f} см")
        print(f"Наличие дефектов: {'да' if self.has_defects else 'нет'}")
        print(f"Многоцветность: {'да' if self.has_defects else 'нет'}")

    def input_breed(self):
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




