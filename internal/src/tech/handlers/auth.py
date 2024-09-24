import datetime
import logging
from typing import Optional

from core.auth.schema.auth import Token
from tech.utils.types import UserConsoleInfo
from tech.handlers.input import InputHandler
from tech.utils.lang.langmodel import LanguageModel
from auth_provider.utils.exceptions import AuthProviderError
from core.auth.schema.auth import AuthSchemaSignIn, AuthDetails
from core.auth.service.auth import IAuthService
from core.user.service.user import IUserService
from core.utils.exceptions import NotFoundRepoError, AuthServiceError, SignInNotFoundEmailError, SignInPasswordError
from core.utils.types import Email, Fingerprint


class AuthHandler:
    auth_service: IAuthService
    lm: LanguageModel
    input_handler: InputHandler
    user_service: IUserService

    def __init__(self, auth_service: IAuthService,
                 user_service: IUserService,
                 input_handler: InputHandler):
        self.input_handler = input_handler
        self.auth_service = auth_service
        self.user_service = user_service
        self.lm = input_handler.lang_model

    def signin(self) -> Optional[UserConsoleInfo]:
        logging.info('auth handler: sign in')
        while True:
            email = self.input_handler.ask_question(self.lm.out_login)

            try:
                Email(email)
            except ValueError:
                logging.warning('auth handler: sign in: email validation error')
                print(self.lm.input_invalid)
                return None

            password = self.input_handler.ask_question(self.lm.out_password)

            try:
                res_user = self.user_service.get_by_email(Email(email))
            except NotFoundRepoError:
                logging.warning(f'auth handler: sign in: no user with email={email}')
                print(self.lm.user_not_found)
                return None

            try:
                res: AuthDetails = self.auth_service.signin(AuthSchemaSignIn(email=Email(email), password=password,
                                                          fingerprint=Fingerprint(value=str(datetime.datetime.now()))))
            except SignInNotFoundEmailError:
                print(self.lm.user_not_found)
                logging.warning(f'auth handler: sign in: no user with email={email}')
                return None
            except SignInPasswordError:
                print(self.lm.invalid_password)
                logging.warning(f'auth handler: sign in: wrong password, email={email}')
                return None

            return UserConsoleInfo(
                id=res_user.id,
                email=res_user.email,
                role=res_user.role,
                name=res_user.name,
                auth_details=res
            )


    def verify_token(self, token: Token) -> bool:
        logging.info('auth handler: verify token')
        try:
            self.auth_service.verify_token(token)
        except AuthProviderError:
            logging.info('auth handler: wrong token')
            return False
        return True

    def logout(self, token: Token) -> None:
        logging.info('auth handler: logout')
        self.auth_service.logout(token)
