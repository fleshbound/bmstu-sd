from pydantic import BaseModel


class LanguageModel(BaseModel):
    no_empty_field: str
    yes: str
    input_incorrect: str
    question_year: str
    question_month: str
    question_day: str

