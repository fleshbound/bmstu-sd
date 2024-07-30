from pydantic import BaseModel

from utils.types import ID, UserName, HashedPassword, Email, Role


class UserSchema(BaseModel):
    id: ID
    login: Email
    hashed_password: HashedPassword
    role: Role
    name: UserName
    is_archived: bool


class UserSchemaCreate(BaseModel):
    login: Email
    hashed_password: HashedPassword
    role: Role
    name: UserName
    is_archived: bool = False


class UserSchemaUpdate(BaseModel):
    id: ID
    login: Email
    hashed_password: HashedPassword
    role: Role
    name: UserName
    is_archived: bool = False


class UserSchemaUpdateBody(BaseModel):
    login: Email
    hashed_password: HashedPassword
    role: Role
    name: UserName
    is_archived: bool = False
