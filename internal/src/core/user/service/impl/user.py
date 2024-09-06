from typing import List

from pydantic import NonNegativeInt, PositiveInt

from internal.src.core.user.repository.user import IUserRepository
from internal.src.core.user.schema.user import UserSchema, UserSchemaCreate, UserSchemaUpdate
from internal.src.core.user.service.user import IUserService
from internal.src.core.utils.exceptions import NotFoundRepoError, UserServiceError, EmailAlreadyTakenError
from internal.src.core.utils.types import ID, Email


class UserService(IUserService):
    user_repo: IUserRepository

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def is_email_taken(self, email: Email) -> bool:
        try:
            self.user_repo.get_by_email(email.value)
        except NotFoundRepoError:
            return False
        return True

    def create(self, create_user: UserSchemaCreate) -> UserSchema:
        if self.is_email_taken(create_user.email):
            raise EmailAlreadyTakenError(create_user.email)
        cur_user = UserSchema.from_create(create_user)
        return self.user_repo.create(cur_user)

    def update(self,
               update_user: UserSchemaUpdate) -> UserSchema:
        cur_user = self.user_repo.get_by_id(update_user.id)
        cur_user = cur_user.from_update(update_user)
        return self.user_repo.update(cur_user)

    def get_all(self,
                skip: NonNegativeInt = 0,
                limit: PositiveInt = 100) -> List[UserSchema]:
        return self.user_repo.get_all(skip, limit)

    def get_by_id(self, user_id: ID) -> UserSchema:
        return self.user_repo.get_by_id(user_id.value)

    def get_by_email(self, email: Email) -> UserSchema:
        return self.user_repo.get_by_email(email.value)
    