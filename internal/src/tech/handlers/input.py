import datetime
from typing import Optional

from pydantic import PositiveInt

from tech.utils.lang.langmodel import LanguageModel


class InputHandler:
    lang_model: LanguageModel

    def __init__(self, lang_model: LanguageModel):
        self.lang_model = lang_model

    @staticmethod
    def ask_question(query: str) -> str:
        print(query, end='')
        return input('')

    def wait_input(self, question: str, out_question: str) -> Optional[str]:
        input = True
        while input:
            res = self.ask_question(question)
            if res == '' or res == '\n':
                print(self.lang_model.no_empty_field)
            else:
                return res
            out = self.ask_question(out_question)
            if out == '' or out == '\n' or self.lang_model.yes.lower() == out.lower():
                input = False
        return None

    def wait_positive_int(self, question: str, out_question: str) -> Optional[PositiveInt]:
        input = True
        while input:
            res = self.ask_question(question)
            try:
                PositiveInt(res)
            except ValueError:
                print(self.lang_model.input_invalid)
            else:
                return res
            out = self.ask_question(out_question)
            if out == '' or out == '\n' or self.lang_model.yes.lower() == out.lower():
                input = False
        return None

    def date_input(self, out_question: str) -> Optional[datetime.datetime]:
        input = True
        while input:
            day = self.ask_question(self.lang_model.question_day)
            month = self.ask_question(self.lang_model.question_month)
            year = self.ask_question(self.lang_model.question_year)

            if day == '' or day == '\n' or month == '' or month == '\n' or year == '' or year == '\n':
                print(self.lang_model.no_empty_field)
            else:
                try:
                    PositiveInt(day)
                    PositiveInt(month)
                    PositiveInt(year)
                except ValueError:
                    print(self.lang_model.input_invalid)
                else:
                    try:
                        date = datetime.datetime(PositiveInt(year), PositiveInt(month), PositiveInt(day))
                    except ValueError:
                        print(self.lang_model.input_invalid)
                    else:
                        return date
            out = self.ask_question(out_question)
            if out == '' or out == '\n' or self.lang_model.yes.lower() == out.lower():
                input = False
        return None
