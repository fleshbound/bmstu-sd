from abc import abstractmethod, ABC
from typing import List

from pydantic import NonNegativeInt

from core.show.schema.show import ShowSchema


class IShowRepository(ABC):
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ShowSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: NonNegativeInt) -> ShowSchema:
        raise NotImplementedError

    @abstractmethod
    def get_by_standard_id(self, standard_id: NonNegativeInt) -> List[ShowSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_breed_id(self, breed_id: NonNegativeInt) -> List[ShowSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_species_id(self, species_id: NonNegativeInt) -> List[ShowSchema]:
        raise NotImplementedError

    @abstractmethod
    def create(self, object: ShowSchema) -> ShowSchema:
        raise NotImplementedError

    @abstractmethod
    def update(self, object: ShowSchema) -> ShowSchema:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: NonNegativeInt) -> None:
        raise NotImplementedError
