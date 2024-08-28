from abc import ABC, abstractmethod
from typing import List

from core.show.schema.usershow import UserShowSchemaCreate, UserShowSchema, UserShowSchemaDelete
from core.utils.types import ID


class IUserShowService(ABC):
    @abstractmethod
    def create(self, usershow_create: UserShowSchemaCreate) -> UserShowSchema:
        raise NotImplementedError

    @abstractmethod
    def archive(self, usershow_id: ID) -> UserShowSchema:
        raise NotImplementedError

    @abstractmethod
    def delete(self, usershow_id: ID) -> UserShowSchemaDelete:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: ID) -> UserShowSchema:
        raise NotImplementedError

    @abstractmethod
    def get_by_user_id(self, user_id: ID) -> List[UserShowSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_show_id(self, show_id: ID) -> List[UserShowSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_user_show_id(self, user_id: ID, show_id: ID) -> UserShowSchema:
        raise NotImplementedError
