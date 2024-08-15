from dataclasses import dataclass

from pydantic import BaseModel

from core.user.schema.user import UserRole
from core.utils.types import ID, UserName, Email, HashedPassword


@dataclass(frozen=True)
class Token:
    value: str

    def __eq__(self, other) -> bool:
        if not isinstance(other, Token):
            return False
        return other.value == self.value

    def __gt__(self, other) -> bool:
        return self.value > other.value


@dataclass(frozen=True)
class Fingerprint:
    value: str

    def __eq__(self, other) -> bool:
        if not isinstance(other, Fingerprint):
            return False
        return other.value == self.value

    def __gt__(self, other) -> bool:
        return self.value > other.value


@dataclass(frozen=True)
class AuthDetails:
    access_token: Token
    refresh_token: Token


@dataclass(frozen=True)
class AuthPayload:
    user_id: ID


class AuthSchemaSignIn(BaseModel):
    email: Email
    password: str
    fingerprint: Fingerprint


class AuthSchemaSignUp(BaseModel):
    id: ID
    email: Email
    password: str
    role: UserRole
    name: UserName
