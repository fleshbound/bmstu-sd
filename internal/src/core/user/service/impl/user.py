from typing import List
import logging
from pydantic import NonNegativeInt, PositiveInt
from sqlalchemy.testing.plugin.plugin_base import logging

from core.user.repository.user import IUserRepository
from core.user.schema.user import UserSchema, UserSchemaCreate, UserSchemaUpdate
from core.user.service.user import IUserService
from core.utils.exceptions import EmailAlreadyTakenError, \
    TooManyResultsRepoError
from core.utils.types import ID, Email

from core.utils.exceptions import NotFoundRepoError


class UserService(IUserService):
    user_repo: IUserRepository

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def is_email_taken(self, email: Email) -> bool:
        try:
            self.user_repo.get_by_email(email.value)
        except TooManyResultsRepoError:
            return True
        except NotFoundRepoError:
            return False
        return False

    def create(self, create_user: UserSchemaCreate) -> UserSchema:
        logging.info('create user')
        if self.is_email_taken(create_user.email):
            logging.warning(f'error create user, email is taken, email={create_user.email.value}')
            raise EmailAlreadyTakenError(create_user.email)
        cur_user = UserSchema.from_create(create_user)
        return self.user_repo.create(cur_user)

    def update(self,
               update_user: UserSchemaUpdate) -> UserSchema:
        logging.info(f'update user, id={update_user.id.value}')
        cur_user = self.user_repo.get_by_id(update_user.id.value)
        cur_user = cur_user.from_update(update_user)
        return self.user_repo.update(cur_user)

    def get_all(self,
                skip: NonNegativeInt = 0,
                limit: PositiveInt = 100) -> List[UserSchema]:
        logging.info(f'get all users, skip={skip} limit={limit}')
        return self.user_repo.get_all(skip, limit)

    def get_by_id(self, user_id: ID) -> UserSchema:
        logging.info(f'get user by id={user_id.value}')
        return self.user_repo.get_by_id(user_id.value)

    def get_by_email(self, email: Email) -> UserSchema:
        logging.info(f'get user by email={email.value}')
        return self.user_repo.get_by_email(email.value)
    