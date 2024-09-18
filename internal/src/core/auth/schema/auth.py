from pydantic import BaseModel

from core.user.schema.user import UserRole
from core.utils.types import ID, UserName, Email, Token, Fingerprint


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
