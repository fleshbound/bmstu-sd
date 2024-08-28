from abc import abstractmethod, ABC
from typing import List

from pydantic import NonNegativeInt

<<<<<<< HEAD
from internal.src.core.animal.schema.animal import AnimalSchema, AnimalSchemaCreate, AnimalSchemaUpdate
||||||| parent of fb32d3b (tests arent working watahel)
from core.animal.schema.animal import AnimalSchema, AnimalSchemaCreate, AnimalSchemaUpdate
=======
from core.animal.schema.animal import AnimalSchema
>>>>>>> fb32d3b (tests arent working watahel)


class IAnimalRepository(ABC):
    @abstractmethod
    def get_by_user_id(self, user_id: NonNegativeInt) -> List[AnimalSchema]:
        raise NotImplementedError
               
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[AnimalSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: NonNegativeInt) -> AnimalSchema:
        raise NotImplementedError

    @abstractmethod
    def create(self, other: AnimalSchema) -> AnimalSchema:
        raise NotImplementedError

    @abstractmethod
    def update(self, other: AnimalSchema) -> AnimalSchema:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: NonNegativeInt) -> None:
        raise NotImplementedError
