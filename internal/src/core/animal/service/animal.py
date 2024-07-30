from abc import ABC, abstractmethod
from typing import List

from pydantic import NonNegativeInt, PositiveInt

from core.animal.schema.animal import AnimalSchema, AnimalSchemaUpdate, AnimalSchemaCreate, AnimalSchemaDelete
from utils.types import ID


class IAnimalService(ABC):
    @abstractmethod
    def archive(self,
                animal_id: ID) -> AnimalSchema:
        raise NotImplementedError

    @abstractmethod
    def create(self,
               create_animal: AnimalSchemaCreate) -> AnimalSchema:
        raise NotImplementedError

    @abstractmethod
    def update(self,
               update_animal: AnimalSchemaUpdate) -> AnimalSchema:
        raise NotImplementedError

    @abstractmethod
    def get_all(self,
                skip: NonNegativeInt = 0,
                limit: PositiveInt = 100) -> List[AnimalSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_user_id(self,
                       user_id: ID) -> List[AnimalSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, animal_id: ID) -> AnimalSchema:
        raise NotImplementedError
