from abc import ABC, abstractmethod
from typing import List

from pydantic import NonNegativeInt, PositiveInt

from core.breed.schema.breed import BreedSchema, BreedSchemaUpdate, BreedSchemaCreate
from utils.types import ID


class IBreedService(ABC):
    @abstractmethod
    def delete(self,
                breed_id: ID) -> BreedSchema:
        raise NotImplementedError

    @abstractmethod
    def create(self,
               create_breed: BreedSchemaCreate) -> BreedSchema:
        raise NotImplementedError

    @abstractmethod
    def update(self,
               update_breed: BreedSchemaUpdate) -> BreedSchema:
        raise NotImplementedError

    @abstractmethod
    def get_all(self,
                skip: NonNegativeInt = 0,
                limit: PositiveInt = 100) -> List[BreedSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_species_id(self,
                          species_id: ID) -> List[BreedSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, breed_id: ID) -> BreedSchema:
        raise NotImplementedError
