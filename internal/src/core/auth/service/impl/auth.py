from core.auth.provider.auth import IAuthProvider
from core.auth.schema.auth import AuthSchemaSignIn, AuthSchemaSignUp, AuthPayload, AuthDetails
from core.auth.service.auth import IAuthService
from core.user.schema.user import UserSchemaCreate
from core.user.service.user import IUserService
from core.utils.exceptions import NotFoundRepoError, SignInNotFoundEmailError, \
    SignInPasswordError
from core.utils.types import Token, Fingerprint
import logging


class AuthService(IAuthService):
    user_service: IUserService
    auth_provider: IAuthProvider

    def __init__(self,
                 user_service: IUserService,
                 auth_provider: IAuthProvider):
        self.user_service = user_service
        self.auth_provider = auth_provider

    def logout(self, token: Token) -> None:
        logging.info(f'logout token={token.value}')
        self.auth_provider.delete_jwt_session(token)

    def signin(self, signin_param: AuthSchemaSignIn) -> AuthDetails:
        logging.info(f'sign in email={signin_param.email.value}')
        try:
            cur_user = self.user_service.get_by_email(signin_param.email)
        except NotFoundRepoError:
            logging.warning(f'sign in email={signin_param.email.value} not found')
            raise SignInNotFoundEmailError(signin_param.email)

        if cur_user.hashed_password.value != self.auth_provider.generate_password_hash(signin_param.password).value:
            logging.warning(f'sing in wrong password')
            raise SignInPasswordError()

        return self.auth_provider.create_jwt_session(AuthPayload(user_id=cur_user.id), signin_param.fingerprint)

    def signup(self, singup_param: AuthSchemaSignUp) -> None:
        logging.info(f'sign up email={singup_param.email.value}')
        user = UserSchemaCreate(email=singup_param.email,
                                hashed_password=self.auth_provider.generate_password_hash(singup_param.password),
                                role=singup_param.role, name=singup_param.name, is_archived=False)
        self.user_service.create(user)

    def refresh_token(self, refresh_token: Token, fingerprint: Fingerprint) -> AuthDetails:
        logging.info('refresh token')
        return self.auth_provider.refresh_jwt_session(refresh_token, fingerprint)

    def verify_token(self, token: Token) -> None:
        logging.info('verify token')
        self.auth_provider.verify_jwt_token(token)

    def payload(self, token: Token) -> AuthPayload:
        return self.auth_provider.verify_jwt_token(token)
