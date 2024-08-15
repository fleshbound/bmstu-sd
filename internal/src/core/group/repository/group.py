from abc import abstractmethod, ABC
from typing import List

from pydantic import NonNegativeInt

from core.group.schema.group import GroupSchema


class IGroupRepository(ABC):
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[GroupSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: NonNegativeInt) -> GroupSchema:
        raise NotImplementedError

    @abstractmethod
    def create(self, object: GroupSchema) -> GroupSchema:
        raise NotImplementedError

    @abstractmethod
    def update(self, object: GroupSchema) -> GroupSchema:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: NonNegativeInt) -> None:
        raise NotImplementedError
