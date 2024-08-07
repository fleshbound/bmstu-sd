import enum

from pydantic import BaseModel

from utils.types import ID, UserName, HashedPassword, Email


@enum.unique
class UserRole(str, enum.Enum):
    admin = "admin"
    guest = "guest"
    breeder = "breeder"
    judge = "judge"


class UserSchema(BaseModel):
    id: ID
    login: Email
    hashed_password: HashedPassword
    role: UserRole
    name: UserName
    is_archived: bool


class UserSchemaCreate(BaseModel):
    login: Email
    hashed_password: HashedPassword
    role: UserRole
    name: UserName
    is_archived: bool = False


class UserSchemaUpdate(BaseModel):
    id: ID
    login: Email
    hashed_password: HashedPassword
    role: UserRole
    name: UserName
    is_archived: bool = False
