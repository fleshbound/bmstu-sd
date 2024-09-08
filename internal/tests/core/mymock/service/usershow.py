from typing import List

from internal.src.core.show.schema.usershow import UserShowSchemaCreate, UserShowSchema, UserShowSchemaDeleted
from internal.src.core.show.service.usershow import IUserShowService
from internal.src.core.utils.exceptions import NotFoundRepoError
from internal.src.core.utils.types import ID


class MockedUserShowService(IUserShowService):
    _usershows: List[UserShowSchema]

    def __init__(self, usershows: List[UserShowSchema]):
        self._usershows = usershows

    def create(self, usershow_create: UserShowSchemaCreate) -> UserShowSchema:
        self._usershows.append(UserShowSchema.from_create(usershow_create))
        if len(self._usershows) > 0:
            self._usershows[-1].id = ID(len(self._usershows) - 1)
        else:
            self._usershows[-1].id = ID(0)
        return self._usershows[-1]

    def archive(self, usershow_id: ID) -> UserShowSchema:
        for record in self._usershows:
            if record.id == usershow_id:
                record.is_archived = True
                return record
        raise NotFoundRepoError(detail='')
        # return UserShowSchema(
        #     id=usershow_id,
        #     user_id=ID(0),
        #     show_id=ID(0),
        #     is_archived=True
        # )

    def delete(self, usershow_id: ID) -> UserShowSchemaDeleted:
        for i, record in enumerate(self._usershows):
            if record.id == usershow_id:
                self._usershows.pop(i)
                return UserShowSchemaDeleted(id=usershow_id)
        return UserShowSchemaDeleted(id=usershow_id)

    def get_by_id(self, id: ID) -> UserShowSchema:
        for record in self._usershows:
            if record.id == id:
                return record
        raise NotFoundRepoError(detail='')
        # return UserShowSchema(
        #     id=id,
        #     user_id=ID(0),
        #     show_id=ID(0),
        #     is_archived=False
        # )

    def get_by_user_id(self, user_id: ID) -> List[UserShowSchema]:
        res = []
        for record in self._usershows:
            if record.user_id == user_id:
                res.append(record)
        if len(res) == 0:
            raise NotFoundRepoError(detail='')
        return res
        # return [UserShowSchema(
        #     id=ID(0),
        #     user_id=user_id,
        #     show_id=ID(0),
        #     is_archived=False
        # )]

    def get_by_show_id(self, show_id: ID) -> List[UserShowSchema]:
        res = []
        for record in self._usershows:
            if record.show_id == show_id:
                res.append(record)
        if len(res) == 0:
            raise NotFoundRepoError()
        return res
        # return [UserShowSchema(
        #     id=ID(0),
        #     user_id=ID(0),
        #     show_id=show_id,
        #     is_archived=False
        # )]

    def get_by_user_show_id(self, user_id: ID, show_id: ID) -> UserShowSchema:
        for record in self._usershows:
            if record.show_id == show_id and record.user_id == user_id:
                return record
        raise NotFoundRepoError()
        # return UserShowSchema(
        #     id=ID(0),
        #     user_id=user_id,
        #     show_id=show_id,
        #     is_archived=False
        # )
