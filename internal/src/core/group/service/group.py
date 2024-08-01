from abc import ABC, abstractmethod
from typing import List

from pydantic import NonNegativeInt, PositiveInt

from core.group.schema.group import GroupSchema, GroupSchemaUpdate, GroupSchemaCreate
from utils.types import ID


class IGroupService(ABC):
    @abstractmethod
    def delete(self,
                group_id: ID) -> GroupSchema:
        raise NotImplementedError

    @abstractmethod
    def create(self,
               create_group: GroupSchemaCreate) -> GroupSchema:
        raise NotImplementedError

    @abstractmethod
    def update(self,
               update_group: GroupSchemaUpdate) -> GroupSchema:
        raise NotImplementedError

    @abstractmethod
    def get_all(self,
                skip: NonNegativeInt = 0,
                limit: PositiveInt = 100) -> List[GroupSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, group_id: ID) -> GroupSchema:
        raise NotImplementedError
