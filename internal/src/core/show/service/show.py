from abc import ABC, abstractmethod
from typing import List

from core.show.schema.show import ShowSchemaCreate, ShowSchema, ShowSchemaUpdate, ShowSchemaDetailed, \
    ShowRegisterAnimalResult
from utils.types import ID


class IShowService(ABC):
    @abstractmethod
    def create(self, show_create: ShowSchemaCreate) -> ShowSchema:
        raise NotImplementedError

    @abstractmethod
    def start(self, show_id: ID) -> ShowSchema:
        raise NotImplementedError

    @abstractmethod
    def abort(self, show_id: ID) -> ShowSchema:
        raise NotImplementedError

    @abstractmethod
    def stop(self, show_id: ID) -> ShowSchema:
        raise NotImplementedError

    @abstractmethod
    def update(self, show_update: ShowSchemaUpdate) -> ShowSchema:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[ShowSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, show_id: ID) -> ShowSchema:
        raise NotImplementedError

    @abstractmethod
    def get_by_user_id(self, user_id: ID) -> ShowSchema:
        raise NotImplementedError

    @abstractmethod
    def get_by_animal_id(self, animal_id: ID) -> ShowSchema:
        raise NotImplementedError

    @abstractmethod
    def get_by_id_detailed_animals(self) -> ShowSchemaDetailed:
        raise NotImplementedError

    @abstractmethod
    def get_by_id_detailed_users(self) -> ShowSchemaDetailed:
        raise NotImplementedError

    @abstractmethod
    def register_animal(self, animal_id: ID, show_id: ID) -> ShowRegisterAnimalResult:
        raise NotImplementedError
