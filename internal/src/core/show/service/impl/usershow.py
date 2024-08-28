from typing import List

<<<<<<< HEAD
<<<<<<< HEAD
from internal.src.core.show.repository.usershow import IUserShowRepository
from internal.src.core.show.schema.usershow import UserShowSchemaCreate, UserShowSchema, UserShowSchemaDeleted
from internal.src.core.show.service.usershow import IUserShowService
from internal.src.core.utils.exceptions import UserShowServiceError
from internal.src.core.utils.types import ID
||||||| parent of fb32d3b (tests arent working watahel)
from core.show.repository.usershow import IUserShowRepository
from core.show.schema.usershow import UserShowSchemaCreate, UserShowSchema, UserShowSchemaDelete
from core.show.service.usershow import IUserShowService
from core.utils.types import ID
=======
from core.show.repository.usershow import IUserShowRepository
from core.show.schema.usershow import UserShowSchemaCreate, UserShowSchema, UserShowSchemaDelete
from core.show.service.usershow import IUserShowService
from core.utils.exceptions import UserShowServiceError
from core.utils.types import ID
>>>>>>> fb32d3b (tests arent working watahel)
||||||| parent of d8bdfb9 (add animal tests (init))
from core.show.repository.usershow import IUserShowRepository
from core.show.schema.usershow import UserShowSchemaCreate, UserShowSchema, UserShowSchemaDelete
from core.show.service.usershow import IUserShowService
from core.utils.exceptions import UserShowServiceError
from core.utils.types import ID
=======
from internal.src.core.show.repository.usershow import IUserShowRepository
from internal.src.core.show.schema.usershow import UserShowSchemaCreate, UserShowSchema, UserShowSchemaDelete
from internal.src.core.show.service.usershow import IUserShowService
from internal.src.core.utils.exceptions import UserShowServiceError
from internal.src.core.utils.types import ID
>>>>>>> d8bdfb9 (add animal tests (init))


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

    def delete(self, usershow_id: ID) -> UserShowSchemaDeleted:
        self.usershow_repo.delete(usershow_id)
        return UserShowSchemaDeleted(id=usershow_id)

    def get_by_id(self, id: ID) -> UserShowSchema:
        return self.usershow_repo.get_by_id(id.value)

    def get_by_user_id(self, user_id: ID) -> List[UserShowSchema]:
        return self.usershow_repo.get_by_user_id(user_id.value)

    def get_by_show_id(self, show_id: ID) -> List[UserShowSchema]:
        return self.usershow_repo.get_by_show_id(show_id.value)

    def get_by_user_show_id(self, user_id: ID, show_id: ID) -> UserShowSchema:
        res = self.usershow_repo.get_by_user_show_id(user_id.value, show_id.value)
        if len(res) > 1:
            raise UserShowServiceError(detail='More than one usershow record')
        return res[0]
