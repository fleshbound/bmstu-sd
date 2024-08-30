from pydantic import BaseModel

<<<<<<< HEAD
<<<<<<< HEAD
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
||||||| parent of d8bdfb9 (add animal tests (init))
from core.user.schema.user import UserRole
from core.utils.types import ID, UserName, Email
=======
||||||| parent of 9dbb4c9 (fix imports)
=======
<<<<<<< HEAD
>>>>>>> 9dbb4c9 (fix imports)
from internal.src.core.user.schema.user import UserRole
from internal.src.core.utils.types import ID, UserName, Email
<<<<<<< HEAD
>>>>>>> d8bdfb9 (add animal tests (init))
||||||| parent of 9dbb4c9 (fix imports)
=======
||||||| parent of 34b5142 (fix imports)
from core.user.schema.user import UserRole
from core.utils.types import ID, UserName, Email, HashedPassword
=======
from internal.src.core.user.schema.user import UserRole
from internal.src.core.utils.types import ID, UserName, Email, HashedPassword
>>>>>>> 34b5142 (fix imports)
>>>>>>> 9dbb4c9 (fix imports)


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
