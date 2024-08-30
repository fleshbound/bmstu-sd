from abc import ABC, abstractmethod
from typing import List

<<<<<<< HEAD
from internal.src.core.show.schema.usershow import UserShowSchemaCreate, UserShowSchema, UserShowSchemaDeleted
from internal.src.core.utils.types import ID
||||||| parent of 34b5142 (fix imports)
from core.show.schema.usershow import UserShowSchemaCreate, UserShowSchema, UserShowSchemaDelete
from core.utils.types import ID
=======
from internal.src.core.show.schema.usershow import UserShowSchemaCreate, UserShowSchema, UserShowSchemaDelete
from internal.src.core.utils.types import ID
>>>>>>> 34b5142 (fix imports)


class IUserShowService(ABC):
    @abstractmethod
    def create(self, usershow_create: UserShowSchemaCreate) -> UserShowSchema:
        raise NotImplementedError

    @abstractmethod
    def archive(self, usershow_id: ID) -> UserShowSchema:
        raise NotImplementedError

    @abstractmethod
    def delete(self, usershow_id: ID) -> UserShowSchemaDeleted:
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
