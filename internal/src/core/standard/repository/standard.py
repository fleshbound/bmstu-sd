from abc import abstractmethod, ABC
from typing import List

from pydantic import NonNegativeInt

from internal.src.core.standard.schema.standard import StandardSchema, StandardSchemaCreate


class IStandardRepository(ABC):
    @abstractmethod
    def get_by_breed_id(self, breed_id: NonNegativeInt) -> List[StandardSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[StandardSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: NonNegativeInt) -> StandardSchema:
        raise NotImplementedError

    @abstractmethod
    def create(self, object: StandardSchema) -> StandardSchema:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: NonNegativeInt) -> None:
        raise NotImplementedError

    # @abstractmethod
    # def update(self, object: StandardSchema) -> StandardSchema:
    #     raise NotImplementedError
