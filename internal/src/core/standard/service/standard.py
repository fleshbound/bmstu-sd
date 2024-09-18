from abc import abstractmethod, ABC
from typing import List

from pydantic import PositiveInt, NonNegativeInt

from core.animal.schema.animal import AnimalSchema
from core.standard.schema.standard import StandardSchema, StandardSchemaCreate, \
    StandardSchemaDeleteResponse
from core.utils.types import ID


class IStandardService(ABC):
    @abstractmethod
    def get_by_breed_id(self, breed_id: ID) -> List[StandardSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, skip: NonNegativeInt = 0, limit: PositiveInt = 100) -> List[StandardSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: ID) -> StandardSchema:
        raise NotImplementedError

    @abstractmethod
    def create(self, standard_create: StandardSchemaCreate) -> StandardSchema:
        raise NotImplementedError
    #
    # @abstractmethod
    # def delete(self, id: ID) -> StandardSchemaDeleteResponse:
    #     raise NotImplementedError

    @abstractmethod
    def check_animal_by_standard(self, standard_id: ID, animal: AnimalSchema) -> bool:
        raise NotImplementedError
