from abc import abstractmethod
from typing import List

from pydantic import NonNegativeInt

from core.breed.schema.breed import BreedSchema
from utils.repository.base import IBaseRepository


class IBreedRepository(IBaseRepository):
    @abstractmethod
    def get_by_species_id(self, species_id: NonNegativeInt) -> List[BreedSchema]:
        raise NotImplementedError
