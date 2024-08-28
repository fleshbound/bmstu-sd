import enum

from pydantic import BaseModel

from internal.src.core.utils.types import ID, UserName, HashedPassword, Email


@enum.unique
class UserRole(str, enum.Enum):
    admin = "admin"
    guest = "guest"
    breeder = "breeder"
    judge = "judge"


class UserSchemaCreate(BaseModel):
    email: Email
    hashed_password: HashedPassword
    role: UserRole
    name: UserName


class UserSchemaUpdate(BaseModel):
    id: ID
    email: Email
    hashed_password: HashedPassword
    role: UserRole
    name: UserName


class UserSchema(BaseModel):
    id: ID
    email: Email
    hashed_password: HashedPassword
    role: UserRole
    name: UserName

    @classmethod
    def from_create(cls, other: UserSchemaCreate):
        return cls(
            id=ID(0),
            email=other.email,
            hashed_password=other.hashed_password,
            role=other.role,
            name=other.name
        )

    def from_update(self, other: UserSchemaUpdate):
        return UserSchema(
            id=self.id,
            email=other.email,
            hashed_password=other.hashed_password,
            role=other.role,
            name=other.name
        )
