from typing import Optional, Type

from core.user.schema.user import UserRole
from tech.handlers.animal import AnimalHandler
from tech.handlers.auth import AuthHandler
from tech.handlers.input import InputHandler
from tech.handlers.show import ShowHandler
from tech.handlers.user import UserHandler
from tech.utils.lang.langmodel import LanguageModel
from tech.utils.types import Menus, ConsoleMessage, UserConsoleInfo


class ConsoleHandler:
    user: Optional[UserConsoleInfo]
    animal_handler: AnimalHandler
    user_handler: UserHandler
    show_handler: ShowHandler
    auth_handler: AuthHandler
    input_handler: InputHandler
    lang_model: LanguageModel

    def __init__(self,
                 animal_handler: AnimalHandler,
                 show_handler: ShowHandler,
                 auth_handler: AuthHandler,
                 user_handler: UserHandler,
                 input_handler: InputHandler):
        self.animal_handler = animal_handler
        self.user_handler = user_handler
        self.show_handler = show_handler
        self.auth_handler = auth_handler
        self.input_handler = input_handler
        self.lang_model = self.input_handler.lang_model
        self.user = None

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

            option = self.input_handler.ask_question(Menus.judge_menu.value)
            if option == '0':
                return 0
            elif option == '1':  #
                self.show_handler.get_shows_all()
                return 1
            elif option == '2':  #
                self.show_handler.get_show_result()
                return 1
            elif option == '3':
                # self.auth_handler.logout()
                return 0
            elif option == '4':  #
                self.show_handler.get_animals_by_show()
                return 1
            elif option == '5':  #
                self.show_handler.score_animal(self.user.id.value)
                return 1
            else:
                print(ConsoleMessage.input_invalid.value)

    def select_admin(self) -> Optional[int]:
        run = True
        while run:
            if not self.check_token():
                return None

            option = self.input_handler.ask_question(Menus.admin_menu.value)
            if option == '0':
                return 0
            elif option == '1':  #
                self.show_handler.get_shows_all()
                return 1
            elif option == '2':  #
                self.show_handler.get_show_result()
                return 1
            elif option == '3':
                # self.auth_handler.logout()
                return 0
            elif option == '4':  #
                self.show_handler.create_show()
                return 1
            elif option == '5':  #
                self.show_handler.start_show()
                return 1
            elif option == '6':  #
                self.show_handler.stop_show()
                return 1
            elif option == '7':  #
                self.show_handler.register_user()
                return 1
            elif option == '8':  #
                self.show_handler.unregister_user()
                return 1
            else:
                print(ConsoleMessage.input_invalid.value)

    def select_breeder(self) -> Optional[int]:
        run = True
        while run:
            if not self.check_token():
                return None

            option = self.input_handler.ask_question(Menus.breeder_menu.value)
            if option == '0':
                return 0
            elif option == '1':  #
                self.show_handler.get_shows_all()
                return 1
            elif option == '2':  #
                self.show_handler.get_show_result()
                return 1
            elif option == '3':
                # self.auth_handler.logout()
                return 0
            elif option == '4':  #
                self.animal_handler.get_animals_by_user_id(self.user.id.value)
                return 1
            elif option == '5':  #
                self.animal_handler.create_animal(self.user.id.value)
                return 1
            elif option == '6':  #
                self.animal_handler.delete_animal()
                return 1
            elif option == '7':  #
                self.show_handler.register_animal()
                return 1
            elif option == '8':  #
                self.show_handler.unregister_animal()
                return 1
            else:
                print(ConsoleMessage.input_invalid.value)

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
            option = self.input_handler.ask_question(Menus.guest_menu.value)
            if option == '0':
                return 0
            elif option == '1':  #
                self.show_handler.get_shows_all()
                return 1
            elif option == '2':  #
                self.show_handler.get_show_result()
                return 1
            elif option == '3':
                res_user = self.auth_handler.signin()
                if res_user is not None:
                    self.set_user(res_user)
                return 1
            elif option == '4':
                self.auth_handler.signup()
                return 1
            else:
                print(ConsoleMessage.input_invalid.value)

    def run(self):
        stop = False
        while not stop:
            code = 1
            if self.user is None:
                code = self.select_guest()
            elif self.user.role == UserRole.breeder:
                code = self.select_breeder()
            elif self.user.role == UserRole.judge:
                code = self.select_judge()
            elif self.user.role == UserRole.admin:
                code = self.select_admin()

            if code == 0:
                stop = True
