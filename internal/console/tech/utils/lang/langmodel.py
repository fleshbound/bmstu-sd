from pydantic import BaseModel


class LanguageModel(BaseModel):
    no_empty_field: str
    yes: str
    input_invalid: str
    question_year: str
    question_month: str
    question_day: str
    auth_token_expired: str
    get_animals_empty_result: str
    question_animal_name: str
    out_question_animal_name: str
    question_animal_breed_id: str
    out_question_animal_breed_id: str
    cancel_input: str
