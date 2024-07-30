from abc import abstractmethod
from typing import List

from pydantic import NonNegativeInt

from core.animal.schema.animal import AnimalSchema
from utils.repository.base import IBaseRepository
from utils.types import ID


class IAnimalRepository(IBaseRepository):
    @abstractmethod
    def get_by_user_id(self, user_id: NonNegativeInt) -> List[AnimalSchema]:
        raise NotImplementedError
