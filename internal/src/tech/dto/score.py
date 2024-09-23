import datetime
from typing import Optional

from tech.handlers.input import InputHandler
from tech.utils.exceptions import CancelInput, InvalidScoreInput
from tech.utils.lang.langmodel import LanguageModel
from core.show.schema.score import ScoreSchemaCreate
from core.utils.types import MAX_SCORE_VALUE, Datetime, ScoreValue, ID


class ScoreDTO:
    id: int
    usershow_id: int
    animalshow_id: int
    value: int
    is_archived: bool
    dt_created: datetime.datetime
    input_handler: InputHandler
    lm: LanguageModel

    def __init__(self,
                 id: Optional[int] = None,
                 usershow_id: Optional[int] = None,
                 animalshow_id: Optional[int] = None,
                 dt_created: Optional[datetime.datetime] = None,
                 value: Optional[int] = None,
                 is_archived: Optional[bool] = None,
                 input_handler: Optional[InputHandler] = None):
        if input_handler is not None:
            self.input_handler = input_handler
            self.lm = self.input_handler.lang_model
        if id is not None: self.id = id
        if usershow_id is not None: self.usershow_id = usershow_id
        if animalshow_id is not None: self.animalshow_id = animalshow_id
        if dt_created is not None: self.dt_created = dt_created
        if value is not None: self.value = value
        if is_archived is not None: self.is_archived = is_archived

    def input_id(self):
        id = self.input_handler.wait_positive_int(
            self.lm.question_show_id,
            self.lm.out_show_id
        )
        if id is None:
            print(self.lm.cancel_input)
            raise CancelInput('show id input cancel')
        self.id = id

    def input_animalshow_id(self):
        animalshow_id = self.input_handler.wait_positive_int(
            self.lm.question_animalshow_id,
            self.lm.out_animalshow_id
        )
        if animalshow_id is None:
            print(self.lm.cancel_input)
            raise CancelInput('score animalshow_id input cancel')
        self.animalshow_id = animalshow_id

    def input_usershow_id(self):
        usershow_id = self.input_handler.wait_positive_int(
            self.lm.question_usershow_id,
            self.lm.out_usershow_id
        )
        if usershow_id is None:
            print(self.lm.cancel_input)
            raise CancelInput('score usershow_id input cancel')
        self.usershow_id = usershow_id

    def input_value(self):
        value = self.input_handler.wait_positive_int(
            self.lm.question_score_value,
            self.lm.out_score_value
        )
        if value is None:
            print(self.lm.cancel_input)
            raise CancelInput('show value input cancel')
        int_value = int(value)
        if int_value > MAX_SCORE_VALUE or int_value < 1:
            print(self.lm.input_invalid)
            raise InvalidScoreInput('show value invalid input (must be from 1 to 5)')
        self.value = int_value

    def input_create(self, usershow_id: int):
        self.usershow_id = usershow_id
        self.input_animalshow_id()
        self.input_value()
        self.is_archived = False
        self.dt_created = datetime.datetime.now()
        self.id = 0
        return self

    def print(self):
        print("_______________________")
        print(f"{self.lm.out_id}:  {self.id}")
        print(f"{self.lm.out_usershow_id}: {self.usershow_id}")
        print(f"{self.lm.out_animalshow_id}: {self.animalshow_id}")
        print(f"{self.lm.out_score_value}: {self.value}")
        print(f"{self.lm.out_dt_created}: {str(self.dt_created.date())}")
        print(f"{self.lm.out_is_archived}: {self.lm.yes if self.is_archived else self.lm.no}")

    def to_schema_create(self) -> ScoreSchemaCreate:
        return ScoreSchemaCreate(
            usershow_id=ID(self.usershow_id),
            animalshow_id=ID(self.animalshow_id),
            value=ScoreValue(self.value),
            dt_created=Datetime(self.dt_created)
        )
