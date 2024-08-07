from typing import List

from core.show.repository.usershow import IUserShowRepository
from core.show.schema.usershow import UserShowSchemaCreate, UserShowSchema
from core.show.service.usershow import IUserShowService
from utils.types import ID


class UserShowService(IUserShowService):
    usershow_repo: IUserShowRepository

    def __init__(self, usershow_repo: IUserShowRepository):
        self.usershow_repo = usershow_repo

    def create(self, usershow_create: UserShowSchemaCreate) -> UserShowSchema:
        new_usershow = UserShowSchema.from_create(usershow_create)
        return self.usershow_repo.create(new_usershow)

    def archive(self, usershow_id: ID) -> UserShowSchema:
        cur_usershow = self.usershow_repo.get_by_id(usershow_id.value)
        cur_usershow.is_archived = True
        return self.usershow_repo.update(cur_usershow)

    def get_by_id(self, id: ID) -> UserShowSchema:
        return self.usershow_repo.get_by_id(id.value)

    def get_by_user_id(self, user_id: ID) -> List[UserShowSchema]:
        return self.usershow_repo.get_by_user_id(user_id.value)

    def get_by_show_id(self, show_id: ID) -> List[UserShowSchema]:
        return self.usershow_repo.get_by_show_id(show_id.value)

    def get_by_user_show_id(self, user_id: ID, show_id: ID) -> List[UserShowSchema]:
        return self.usershow_repo.get_by_user_show_id(user_id.value, show_id.value)

