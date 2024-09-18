from abc import abstractmethod, ABC
from typing import List

from pydantic import NonNegativeInt

from core.species.schema.species import SpeciesSchema


class ISpeciesRepository(ABC):
    @abstractmethod
    def get_by_group_id(self, group_id: NonNegativeInt) -> List[SpeciesSchema]:
        raise NotImplementedError
               
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[SpeciesSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: NonNegativeInt) -> SpeciesSchema:
        raise NotImplementedError

    @abstractmethod
    def create(self, object: SpeciesSchema) -> SpeciesSchema:
        raise NotImplementedError

    @abstractmethod
    def update(self, object: SpeciesSchema) -> SpeciesSchema:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: NonNegativeInt) -> None:
        raise NotImplementedError
