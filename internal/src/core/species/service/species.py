from abc import ABC, abstractmethod
from typing import List

from pydantic import NonNegativeInt, PositiveInt

from core.species.schema.species import SpeciesSchema, SpeciesSchemaUpdate, SpeciesSchemaCreate
from utils.types import ID


class ISpeciesService(ABC):
    @abstractmethod
    def delete(self,
                species_id: ID) -> SpeciesSchema:
        raise NotImplementedError

    @abstractmethod
    def create(self,
               create_species: SpeciesSchemaCreate) -> SpeciesSchema:
        raise NotImplementedError

    @abstractmethod
    def update(self,
               update_species: SpeciesSchemaUpdate) -> SpeciesSchema:
        raise NotImplementedError

    @abstractmethod
    def get_all(self,
                skip: NonNegativeInt = 0,
                limit: PositiveInt = 100) -> List[SpeciesSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_group_id(self,
                        group_id: ID) -> List[SpeciesSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, species_id: ID) -> SpeciesSchema:
        raise NotImplementedError
