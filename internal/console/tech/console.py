from typing import Optional

from pydantic import BaseModel

from internal.src.core.auth.schema.auth import AuthDetails
from internal.src.core.user.schema.user import UserRole
from internal.src.core.utils.types import ID, UserName, Email
from internal.console.tech.handler.animal import AnimalHandler
from internal.console.tech.handler.auth import AuthHandler
from internal.console.tech.handler.input import InputHandler
from internal.console.tech.handler.show import ShowHandler
from internal.console.tech.handler.user import UserHandler
from internal.console.tech.utils.lang.langmodel import LanguageModel
from internal.console.tech.utils.types import Menus, ConsoleMessage


class UserConsoleInfo(BaseModel):
    id: Optional[ID]
    email: Optional[Email]
    role: Optional[UserRole]
    name: Optional[UserName]
    auth_details: Optional[AuthDetails]


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

    def check_token(self) -> bool:
        if not self.auth_handler.verify_token(self.user.auth_details.access_token):
            print(self.lang_model.auth_token_expired)
            return False
        return True

    def select_judge(self) -> Optional[int]:
        # 'Выберите пункт меню (Судья):\n'\
        #                   '0. Завершить работу\n'\
        #                   '1. Посмотреть список выставок\n'\
        #                   '2. Посмотреть результаты выставки\n'\
        #                   '3. Выйти\n'\
        #                   '4. Посмотреть участников выставки\n'\
        #                   '5. Оценить участника выставки\n'
        run = True
        while run:
            if not self.check_token():
                return None

            option = self.input_handler.ask_question(self.menus.judge_menu)
            if option == '0':
                return 0
            elif option == '1':
                self.show_handler.get_shows_all()
                return 1
            elif option == '2':
                self.show_handler.get_show_result()
                return 1
            elif option == '3':
                self.auth_handler.logout()
                return 1
            elif option == '4':
                self.show_handler.get_animals_by_show()
                return 1
            elif option == '5':
                self.show_handler.score_animal()
                return 1
            else:
                print(ConsoleMessage.input_invalid)

    def select_admin(self) -> Optional[int]:
        run = True
        while run:
            if not self.check_token():
                return None

            option = self.input_handler.ask_question(self.menus.admin_menu)
            if option == '0':
                return 0
            elif option == '1':
                self.show_handler.get_shows_all()
                return 1
            elif option == '2':
                self.show_handler.get_show_result()
                return 1
            elif option == '3':
                self.auth_handler.logout()
                return 1
            elif option == '4':
                self.show_handler.create_show()
                return 1
            elif option == '5':
                self.show_handler.start_show()
                return 1
            elif option == '6':
                self.show_handler.stop_show()
                return 1
            elif option == '7':
                self.show_handler.register_user()
                return 1
            elif option == '8':
                self.show_handler.unregister_user()
                return 1
            else:
                print(ConsoleMessage.input_invalid)

    def select_breeder(self) -> Optional[int]:
        run = True
        while run:
            if not self.check_token():
                return None

            option = self.input_handler.ask_question(self.menus.breeder_menu)
            if option == '0':
                return 0
            elif option == '1':
                self.show_handler.get_shows_all()
                return 1
            elif option == '2':
                self.show_handler.get_show_result()
                return 1
            elif option == '3':
                self.auth_handler.logout()
                return 1
            elif option == '4':
                self.animal_handler.get_animals_by_user_id(self.user.id)
                return 1
            elif option == '5':
                self.animal_handler.create_animal()
                return 1
            elif option == '6':
                self.animal_handler.delete_animal()
                return 1
            elif option == '7':
                self.show_handler.register_animal()
                return 1
            elif option == '8':
                self.show_handler.unregister_animal()
                return 1
            else:
                print(ConsoleMessage.input_invalid)

    def set_user(self, new_user: UserConsoleInfo) -> None:
        self.user.id = new_user.id
        self.user.email = new_user.email
        self.user.role = new_user.role
        self.user.name = new_user.name
        self.user.auth_details = new_user.auth_details

    def unset_user(self) -> None:
        self.user.id = None
        self.user.email = None
        self.user.role = None
        self.user.name = None
        self.user.auth_details = None

    def select_guest(self) -> int:
        run = True
        while run:
            option = self.input_handler.ask_question(self.menus.guest_menu)
            if option == '0':
                return 0
            elif option == '1':
                self.show_handler.get_shows_all()
                return 1
            elif option == '2':
                self.show_handler.get_show_result()
                return 1
            elif option == '3':
                res_user = self.auth_handler.signin()
                if not res_user is None:
                    self.set_user(res_user)
                    return 1
            elif option == '4':
                self.auth_handler.signup()
                return 1
            else:
                print(ConsoleMessage.input_invalid)
