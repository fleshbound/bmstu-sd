from abc import ABC, abstractmethod
from typing import List

from pydantic import NonNegativeInt, PositiveInt

from core.show.schema.show import ShowSchemaCreate, ShowSchema, ShowSchemaUpdate, ShowSchemaDetailed, \
    ShowRegisterAnimalResult, ShowRegisterUserResult
from core.utils.types import ID


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
    def get_all(self, skip: NonNegativeInt = 0, limit: PositiveInt = 100) -> List[ShowSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, show_id: ID) -> ShowSchema:
        raise NotImplementedError

    @abstractmethod
    def get_by_standard_id(self, standard_id: ID) -> List[ShowSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_user_id(self, user_id: ID) -> List[ShowSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_animal_id(self, animal_id: ID) -> List[ShowSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id_detailed(self, show_id: ID) -> ShowSchemaDetailed:
        raise NotImplementedError

    @abstractmethod
    def register_animal(self, animal_id: ID, show_id: ID) -> ShowRegisterAnimalResult:
        raise NotImplementedError

    @abstractmethod
    def register_user(self, user_id: ID, show_id: ID) -> ShowRegisterUserResult:
        raise NotImplementedError

    @abstractmethod
    def unregister_animal(self, animal_id: ID, show_id: ID) -> ShowRegisterAnimalResult:
        raise NotImplementedError

    @abstractmethod
    def unregister_user(self, user_id: ID, show_id: ID) -> ShowRegisterUserResult:
        raise NotImplementedError
