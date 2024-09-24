from typing import List

from pydantic import NonNegativeInt, PositiveInt
from sqlalchemy.testing.plugin.plugin_base import logging

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
        logging.info(f'delete group id={group_id.value}')
        self.group_repo.delete(group_id.value)
        return GroupSchemaDelete(id=group_id)

    def create(self,
               create_group: GroupSchemaCreate) -> GroupSchema:
        logging.info('create group')
        cur_group = GroupSchema.from_create(create_group)
        return self.group_repo.create(cur_group)

    def update(self,
               update_group: GroupSchemaUpdate) -> GroupSchema:
        logging.info(f'update group id={update_group.id.value}')
        cur_group = self.group_repo.get_by_id(update_group.id.value)
        cur_group = cur_group.from_update(update_group)
        return self.group_repo.update(cur_group)

    def get_all(self,
                skip: NonNegativeInt = 0,
                limit: PositiveInt = 100) -> List[GroupSchema]:
        logging.info(f'get all groups skip={skip}, limit={limit}')
        return self.group_repo.get_all(skip, limit)

    def get_by_id(self, group_id: ID) -> GroupSchema:
        logging.info(f'get group by id={group_id.value}')
        return self.group_repo.get_by_id(group_id.value)
