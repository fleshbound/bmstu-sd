from abc import ABC, abstractmethod
from typing import List, TypeVar, Type
from pydantic import BaseModel

from utils.types import NonNegativeInt

T = TypeVar("T", bound=BaseModel)


class IBaseRepository(ABC):
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Type[T]]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: NonNegativeInt) -> Type[T]:
        raise NotImplementedError

    @abstractmethod
    def create(self, object: Type[T]) -> Type[T]:
        raise NotImplementedError

    @abstractmethod
    def update(self, object: Type[T]) -> Type[T]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: NonNegativeInt) -> None:
        raise NotImplementedError
