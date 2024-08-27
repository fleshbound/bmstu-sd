from pydantic import BaseModel

from core.auth.schema.auth import AuthDetails
from core.user.schema.user import UserRole
from core.utils.types import ID, UserName, Email
from internal.petowo.console.tech.animal import AnimalHandler
from internal.petowo.console.tech.auth import AuthHandler
from internal.petowo.console.tech.input import InputHandler
from internal.petowo.console.tech.show import ShowHandler
from internal.petowo.console.tech.user import UserHandler
from internal.petowo.console.tech.utils.lang.langmodel import LanguageModel
from internal.petowo.console.tech.utils.types import Menus


class UserConsoleInfo(BaseModel):
    id: ID
    email: Email
    role: UserRole
    name: UserName
    auth_details: AuthDetails


class ConsoleHandler:
    user: UserConsoleInfo
    animal_handler: AnimalHandler
    user_handler: UserHandler
    show_handler: ShowHandler
    auth_handler: AuthHandler
    menus: Menus
    input_handler: InputHandler
    lang_model: LanguageModel

    def __init__(self,
                 animal_handler: AnimalHandler,
                 show_handler: ShowHandler,
                 auth_handler: AuthHandler,
                 user_handler: UserHandler,
                 lang_model: LanguageModel):
        self.animal_handler = animal_handler
        self.user_handler = user_handler
        self.show_handler = show_handler
        self.auth_handler = auth_handler
        self.lang_model = lang_model
        self.input_handler = InputHandler()

    def print_menu(self):
        pass

    def check_auth(self):
        pass

    def select_breeder(self):
        pass

    # 0. Завершить работу\n'\
    #                   '1. Посмотреть список выставок\n'\
    #                   '2. Посмотреть результаты выставки\n'\
    #                   '3. Войти\n'\
    #                   '4. Зарегистрироваться\n'

    def select_guest(self):
        run = True
        while run:
            print(self.menus.guest_menu)
            if
