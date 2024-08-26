from abc import abstractmethod, ABC

from core.auth.schema.auth import Token, AuthSchemaSignIn, AuthSchemaSignUp, Fingerprint, AuthDetails, AuthPayload


class IAuthService(ABC):
    @abstractmethod
    def logout(self, token: Token) -> None:
        raise NotImplementedError

    @abstractmethod
    def signin(self, signin_param: AuthSchemaSignIn) -> AuthDetails:
        raise NotImplementedError

    @abstractmethod
    def signup(self, singup_param: AuthSchemaSignUp) -> None:
        raise NotImplementedError

    @abstractmethod
    def refresh_token(self, refresh_token: Token, fingerprint: Fingerprint) -> AuthDetails:
        raise NotImplementedError

    @abstractmethod
    def verify_token(self, token: Token) -> None:
        raise NotImplementedError

    @abstractmethod
    def payload(self, token: Token) -> AuthPayload:
        raise NotImplementedError
