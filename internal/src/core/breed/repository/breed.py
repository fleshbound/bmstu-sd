from abc import abstractmethod, ABC
from typing import List

from pydantic import NonNegativeInt

from core.breed.schema.breed import BreedSchema


class IBreedRepository(ABC):
    @abstractmethod
    def get_by_species_id(self, species_id: NonNegativeInt) -> List[BreedSchema]:
        raise NotImplementedError
               
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[BreedSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: NonNegativeInt) -> BreedSchema:
        raise NotImplementedError

    @abstractmethod
    def create(self, object: BreedSchema) -> BreedSchema:
        raise NotImplementedError

    @abstractmethod
    def update(self, object: BreedSchema) -> BreedSchema:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: NonNegativeInt) -> None:
        raise NotImplementedError
