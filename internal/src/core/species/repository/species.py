from abc import abstractmethod
from typing import List

from pydantic import NonNegativeInt

from core.species.schema.species import SpeciesSchema
from utils.repository.base import IBaseRepository


class ISpeciesRepository(IBaseRepository):
    @abstractmethod
    def get_by_group_id(self, group_id: NonNegativeInt) -> List[SpeciesSchema]:
        raise NotImplementedError
