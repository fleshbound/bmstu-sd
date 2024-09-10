from internal.console.tech.utils.lang.langmodel import LanguageModel


class RuLanguageModel(LanguageModel):
    no_empty_field = 'Ввод не может быть пустым'
    yes = 'Да'
    input_invalid = 'Некорректный ввод'
    question_year = 'Введите год: '
    question_month = 'Введите месяц: '
    question_day = 'Введите день: '
    auth_token_expired = 'Время сессии истекло'
    get_animals_empty_result = 'Животные не найдены'
    question_animal_name = 'Введите имя животного: '
    out_question_animal_name = 'Завершить ввод имени животного? '
    question_animal_breed_id = 'Введите ID породы животного: '
    out_question_animal_breed_id = 'Завершить ввод ID породы животного? '
    cancel_input = 'Ввод отменен'
