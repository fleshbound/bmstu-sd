import datetime
from typing import Optional

from core.auth.schema.auth import Token
from tech.console import UserConsoleInfo
from tech.handler.input import InputHandler
from tech.utils.lang.langmodel import LanguageModel
from auth_provider.utils.exceptions import AuthProviderError
from core.auth.schema.auth import AuthSchemaSignIn, AuthDetails
from core.auth.service.auth import IAuthService
from core.user.service.user import IUserService
from core.utils.exceptions import NotFoundRepoError, AuthServiceError
from core.utils.types import Email, Fingerprint


class AuthHandler:
    auth_service: IAuthService
    lm: LanguageModel
    input_handler: InputHandler
    user_service: IUserService
    # def verify_auth_role(self):
    #     raise NotImplementedError

    # def verify_auth(self):
    #     raise NotImplementedError

    def __init__(self, auth_service: IAuthService,
                 user_service: IUserService,
                 input_handler: InputHandler):
        self.input_handler = input_handler
        self.auth_service = auth_service
        self.user_service = user_service
        self.lm = input_handler.lang_model

    def signin(self) -> Optional[UserConsoleInfo]:
        while True:
            email = self.input_handler.ask_question('Логин (почта): ')
            password = self.input_handler.ask_question('Пароль: ')

            try:
                res_user = self.user_service.get_by_email(Email(email))
            except NotFoundRepoError:
                print(self.lm.user_not_found)
                return None

            try:
                res: AuthDetails = self.auth_service.signin(AuthSchemaSignIn(email=Email(email), password=password,
                                                          fingerprint=Fingerprint(value=str(datetime.datetime.now()))))
            except AuthServiceError as e:
                print(e)
                return None

            return UserConsoleInfo(
                id=res_user.id,
                email=res_user.email,
                role=res_user.role,
                name=res_user.name,
                auth_details=res
            )


    def verify_token(self, token: Token) -> bool:
        try:
            self.auth_service.verify_token(token)
        except AuthProviderError:
            return False
        return True

    def signup(self):
        return None

    # def logout(self):
    #     raise NotImplementedError
