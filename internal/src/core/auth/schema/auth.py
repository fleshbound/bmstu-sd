from dataclasses import dataclass

from pydantic import BaseModel

<<<<<<< HEAD
from internal.src.core.user.schema.user import UserRole
from internal.src.core.utils.types import ID, UserName, Email, HashedPassword
||||||| parent of fb32d3b (tests arent working watahel)
from core.user.schema.user import UserRole
from core.utils.types import ID, UserName, Email, HashedPassword
=======
from core.user.schema.user import UserRole
from core.utils.types import ID, UserName, Email
>>>>>>> fb32d3b (tests arent working watahel)


class Token(BaseModel):
    value: str

    def __eq__(self, other) -> bool:
        if not isinstance(other, Token):
            return False
        return other.value == self.value

    def __gt__(self, other) -> bool:
        return self.value > other.value


class Fingerprint(BaseModel):
    value: str

    def __eq__(self, other) -> bool:
        if not isinstance(other, Fingerprint):
            return False
        return other.value == self.value

    def __gt__(self, other) -> bool:
        return self.value > other.value


class AuthDetails(BaseModel):
    access_token: Token
    refresh_token: Token


class AuthPayload(BaseModel):
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
