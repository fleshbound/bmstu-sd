import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass

from pydantic import BaseModel

from internal.src.core.auth.schema.auth import AuthPayload, Token, Fingerprint


class AuthSession(BaseModel):
    refresh_token: Token
    refresh_expire_dt: datetime.datetime
    fingerprint: Token
    payload: AuthPayload


class ISessionStorage(ABC):
    @abstractmethod
    def get(self, refresh_token: str) -> AuthSession:
        raise NotImplementedError

    @abstractmethod
    def put(self, refresh_token: str, session: AuthSession, expire_dt: datetime.timedelta) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, refresh_token: str) -> None:
        raise NotImplementedError
||||||| parent of f29a537 (add auth tests)
=======
import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass

from pydantic import BaseModel

from core.auth.schema.auth import AuthPayload, Token, Fingerprint


class AuthSession(BaseModel):
    refresh_token: Token
    refresh_expire_dt: datetime.datetime
    fingerprint: Token
    payload: AuthPayload


class ISessionStorage(ABC):
    @abstractmethod
    def get(self, refresh_token: str) -> AuthSession:
        raise NotImplementedError

    @abstractmethod
    def put(self, refresh_token: str, session: AuthSession, expire_dt: datetime.timedelta) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, refresh_token: str) -> None:
        raise NotImplementedError
>>>>>>> f29a537 (add auth tests)
