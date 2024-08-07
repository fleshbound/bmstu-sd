from abc import abstractmethod, ABC
from typing import List

from pydantic import NonNegativeInt

from core.show.schema.usershow import UserShowSchema


class IUserShowRepository(ABC):
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[UserShowSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: NonNegativeInt) -> UserShowSchema:
        raise NotImplementedError

    @abstractmethod
    def create(self, object: UserShowSchema) -> UserShowSchema:
        raise NotImplementedError

    @abstractmethod
    def update(self, object: UserShowSchema) -> UserShowSchema:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: NonNegativeInt) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_user_id(self, user_id: NonNegativeInt) -> List[UserShowSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_show_id(self, show_id: NonNegativeInt) -> List[UserShowSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_user_show_id(self, user_id: NonNegativeInt, show_id: NonNegativeInt) -> List[UserShowSchema]:
        raise NotImplementedError
