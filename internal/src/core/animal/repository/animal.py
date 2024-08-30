from abc import abstractmethod, ABC
from typing import List

from pydantic import NonNegativeInt

from internal.src.core.animal.schema.animal import AnimalSchema, AnimalSchemaCreate, AnimalSchemaUpdate


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
