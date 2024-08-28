from abc import ABC, abstractmethod
from typing import List

from pydantic import NonNegativeInt

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
from internal.src.core.user.schema.user import UserSchema
>>>>>>> d8bdfb9 (add animal tests (init))


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
