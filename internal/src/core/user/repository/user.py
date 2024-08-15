from abc import ABC, abstractmethod
from typing import List

from pydantic import NonNegativeInt

from core.user.schema.user import UserSchema, UserSchemaUpdate, UserSchemaCreate


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
