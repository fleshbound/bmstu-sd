from abc import ABC, abstractmethod
from typing import List

from pydantic import NonNegativeInt, PositiveInt

from internal.src.core.user.schema.user import UserSchema, UserSchemaCreate, UserSchemaUpdate
from internal.src.core.utils.types import ID, Email


class IUserService(ABC):
    @abstractmethod
<<<<<<< HEAD
    def delete(self,
                user_id: ID) -> UserSchema:
        raise NotImplementedError

    @abstractmethod
||||||| parent of 1181f99 (add show service tests)
    def archive(self,
                user_id: ID) -> UserSchema:
        raise NotImplementedError

    @abstractmethod
=======
>>>>>>> 1181f99 (add show service tests)
    def create(self,
               create_user: UserSchemaCreate) -> UserSchema:
        raise NotImplementedError

    @abstractmethod
    def update(self,
               update_user: UserSchemaUpdate) -> UserSchema:
        raise NotImplementedError

    @abstractmethod
    def get_all(self,
                skip: NonNegativeInt = 0,
                limit: PositiveInt = 100) -> List[UserSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, user_id: ID) -> UserSchema:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: Email) -> UserSchema:
        raise NotImplementedError
