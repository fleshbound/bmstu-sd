import datetime
from typing import Optional

from pydantic import PositiveInt

from core.utils.types import Datetime
from internal.petowo.console.tech.utils.lang.langmodel import LanguageModel


class InputHandler:
    lang_model: LanguageModel

    def ask_question(self, query: str) -> str:
        print(query)
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
                print(self.lang_model.input_incorrect)
            else:
                return res
            out = self.ask_question(out_question)
            if out == '' or out == '\n' or self.lang_model.yes.lower() == out.lower():
                input = False
        return None

    def date_input(self, out_question: str) -> Optional[Datetime]:
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
                    print(self.lang_model.input_incorrect)
                else:
                    try:
                        date = datetime.datetime(PositiveInt(year), PositiveInt(month), PositiveInt(day))
                    except ValueError:
                        print(self.lang_model.input_incorrect)
