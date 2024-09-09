from internal.console.tech.utils.lang.langmodel import LanguageModel


class RuLanguageModel(LanguageModel):
    no_empty_field = 'Ввод не может быть пустым'
    yes = 'Да'
    input_invalid = 'Некорректный ввод'
    question_year = 'Введите год: '
    question_month = 'Введите месяц: '
    question_day = 'Введите день: '
    auth_token_expired = 'Время сессии истекло'
