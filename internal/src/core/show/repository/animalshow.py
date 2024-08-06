from abc import abstractmethod, ABC
from typing import List

from pydantic import NonNegativeInt

from core.show.schema.animalshow import AnimalShowSchema


class IAnimalShowRepository(ABC):
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[AnimalShowSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: NonNegativeInt) -> AnimalShowSchema:
        raise NotImplementedError

    @abstractmethod
    def create(self, object: AnimalShowSchema) -> AnimalShowSchema:
        raise NotImplementedError

    @abstractmethod
    def update(self, object: AnimalShowSchema) -> AnimalShowSchema:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: NonNegativeInt) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_animal_id(self, animal_id: NonNegativeInt) -> List[AnimalShowSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_show_id(self, show_id: NonNegativeInt) -> List[AnimalShowSchema]:
        raise NotImplementedError
