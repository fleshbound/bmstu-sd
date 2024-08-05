from typing import List

from pydantic import NonNegativeInt

from core.group.schema.group import GroupSchema

from core.group.repository.group import IGroupRepository


class MockedGroupRepository(IGroupRepository):
    _groups: List[GroupSchema]

    def __init__(self, groups: List[GroupSchema]):
        self._groups = groups

    def get_all(self, skip: int = 0, limit: int = 100) -> List[GroupSchema]:
        return self._groups

    def get_by_id(self, id: NonNegativeInt) -> GroupSchema:
        return self._groups[0]

    def create(self, object: GroupSchema) -> GroupSchema:
        self._groups.append(object)
        return object

    def update(self, object: GroupSchema) -> GroupSchema:
        return object

    def delete(self, id: NonNegativeInt) -> None:
        return None
