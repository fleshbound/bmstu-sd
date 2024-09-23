import enum
from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel

from core.auth.schema.auth import AuthDetails
from core.user.schema.user import UserRole
from core.utils.types import ID, Email, UserName


class UserConsoleInfo(BaseModel):
    id: Optional[ID]
    email: Optional[Email]
    role: Optional[UserRole]
    name: Optional[UserName]
    auth_details: Optional[AuthDetails]
    

@dataclass
class Option:
    value: int


@enum.unique
class ConsoleInputStatus(str, enum.Enum):
    ok = 'Корректный ввод'
    invalid = 'Некорректный ввод'


@dataclass
class ConsoleInputResponse:
    res: str
    status: ConsoleInputStatus


@enum.unique
class Menus(str, enum.Enum):
    guest_menu = '\nМеню (Гость):\n'\
                  '0. Завершить работу\n'\
                  '1. Посмотреть список выставок\n'\
                  '2. Посмотреть результаты выставки\n'\
                  '3. Войти\n'\
                  'Выберите пункт: '
    admin_menu = '\nМеню (Организатор):\n'\
                  '0. Завершить работу\n'\
                  '1. Посмотреть список выставок\n'\
                  '2. Посмотреть результаты выставки\n'\
                  '3. Выйти\n'\
                  '4. Создать выставку\n'\
                  '5. Запустить выставку\n'\
                  '6. Завершить выставку\n'\
                  '7. Добавить судью на выставку\n'\
                  '8. Удалить судью с выставки\n'\
                  'Выберите пункт: '
    breeder_menu = '\nМеню (Заводчик):\n'\
                    '0. Завершить работу\n'\
                    '1. Посмотреть список выставок\n'\
                    '2. Посмотреть результаты выставки\n'\
                    '3. Выйти\n'\
                    '4. Список животных\n'\
                    '5. Добавить животное\n'\
                    '6. Удалить животное\n'\
                    '7. Записать животное на выставку\n'\
                    '8. Отписать животное от выставки\n'\
                  'Выберите пункт: '
    judge_menu = '\nМеню (Судья):\n'\
                  '0. Завершить работу\n'\
                  '1. Посмотреть список выставок\n'\
                  '2. Посмотреть результаты выставки\n'\
                  '3. Выйти\n'\
                  '4. Посмотреть участников выставки\n'\
                  '5. Оценить участника выставки\n'\
                  'Выберите пункт: '


@enum.unique
class ConsoleMessage(str, enum.Enum):
    input_invalid: str = 'Ошибка выбора пункта'
