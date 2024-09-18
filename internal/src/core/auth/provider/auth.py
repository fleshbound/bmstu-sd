from abc import ABC, abstractmethod

from core.auth.schema.auth import AuthPayload, AuthDetails
from core.utils.types import HashedPassword, Token, Fingerprint


class IAuthProvider(ABC):
    @abstractmethod
    def create_jwt_session(self, payload: AuthPayload, fingerprint: Fingerprint) -> AuthDetails:
        raise NotImplementedError

    @abstractmethod
    def refresh_jwt_session(self, refresh_token: Token, fingerprint: Fingerprint) -> AuthDetails:
        raise NotImplementedError

    @abstractmethod
    def delete_jwt_session(self, refresh_token: Token) -> None:
        raise NotImplementedError

    @abstractmethod
    def verify_jwt_token(self, access_token: Token) -> AuthPayload:
        raise NotImplementedError

    @abstractmethod
    def generate_password_hash(self, password: str) -> HashedPassword:
        raise NotImplementedError
