from pydantic import Field, BaseModel

from core.user.schema.user import UserSchema, UserRole
from core.utils.types import Email, HashedPassword, UserName, ID
from repository.utils.types import PyObjectId, int_from_pyobject_id


class UserODM(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    email: str
    hashed_password: str
    role: str
    name: str

    def to_schema(self) -> UserSchema:
        return UserSchema(
            id=ID(int_from_pyobject_id(self.id)),
            email=Email(self.email),
            hashed_password=HashedPassword(self.hashed_password),
            role=UserRole(self.role),
            name=UserName(self.name)
        )
