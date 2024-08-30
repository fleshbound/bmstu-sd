from abc import ABC, abstractmethod
from typing import List

from pydantic import NonNegativeInt

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from internal.src.core.user.schema.user import UserSchema, UserSchemaUpdate, UserSchemaCreate
||||||| parent of fb32d3b (tests arent working watahel)
from core.user.schema.user import UserSchema, UserSchemaUpdate, UserSchemaCreate
=======
from core.user.schema.user import UserSchema
>>>>>>> fb32d3b (tests arent working watahel)
||||||| parent of d8bdfb9 (add animal tests (init))
from core.user.schema.user import UserSchema
=======
||||||| parent of 9dbb4c9 (fix imports)
=======
<<<<<<< HEAD
>>>>>>> 9dbb4c9 (fix imports)
from internal.src.core.user.schema.user import UserSchema
<<<<<<< HEAD
>>>>>>> d8bdfb9 (add animal tests (init))
||||||| parent of 9dbb4c9 (fix imports)
=======
||||||| parent of 34b5142 (fix imports)
from core.user.schema.user import UserSchema, UserSchemaUpdate, UserSchemaCreate
=======
from internal.src.core.user.schema.user import UserSchema, UserSchemaUpdate, UserSchemaCreate
>>>>>>> 34b5142 (fix imports)
>>>>>>> 9dbb4c9 (fix imports)


class IUserRepository(ABC):
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[UserSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: NonNegativeInt) -> UserSchema:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> UserSchema:
        raise NotImplementedError

    @abstractmethod
    def create(self, object: UserSchema) -> UserSchema:
        raise NotImplementedError

    @abstractmethod
    def update(self, object: UserSchema) -> UserSchema:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: NonNegativeInt) -> None:
        raise NotImplementedError
