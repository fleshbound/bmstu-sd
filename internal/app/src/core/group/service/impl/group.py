from typing import List

from pydantic import NonNegativeInt, PositiveInt

from core.group.repository.group import IGroupRepository
from core.group.schema.group import GroupSchema, GroupSchemaCreate, GroupSchemaUpdate, GroupSchemaDelete
from core.group.service.group import IGroupService
from core.utils.types import ID


class GroupService(IGroupService):
    group_repo: IGroupRepository

    def __init__(self,
                 group_repo: IGroupRepository):
        self.group_repo = group_repo

    def delete(self,
               group_id: ID) -> GroupSchemaDelete:
        self.group_repo.delete(group_id.value)
        return GroupSchemaDelete(id=group_id)

    def create(self,
               create_group: GroupSchemaCreate) -> GroupSchema:
        cur_group = GroupSchema.from_create(create_group)
        return self.group_repo.create(cur_group)

    def update(self,
               update_group: GroupSchemaUpdate) -> GroupSchema:
        cur_group = self.group_repo.get_by_id(update_group.id.value)
        cur_group = cur_group.from_update(update_group)
        return self.group_repo.update(cur_group)

    def get_all(self,
                skip: NonNegativeInt = 0,
                limit: PositiveInt = 100) -> List[GroupSchema]:
        return self.group_repo.get_all(skip, limit)

    def get_by_id(self, group_id: ID) -> GroupSchema:
        return self.group_repo.get_by_id(group_id.value)
