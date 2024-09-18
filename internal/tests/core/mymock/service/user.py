from typing import List

from pydantic import NonNegativeInt, PositiveInt

from core.user.schema.user import UserSchema, UserSchemaCreate, UserSchemaUpdate
from core.user.service.user import IUserService
from core.utils.exceptions import NotFoundRepoError
from core.utils.types import Email, ID


class MockedUserService(IUserService):
    _users: List[UserSchema]
    
    def __init__(self, users: List[UserSchema]):
        self._users = users
        
    def create(self,
               create_user: UserSchemaCreate) -> UserSchema:
        self._users.append(UserSchema.from_create(create_user))
        return self._users[-1]

    def update(self,
               update_user: UserSchemaUpdate) -> UserSchema:
        for user in self._users:
            if user.id == update_user.id:
                user = user.from_update(update_user)
                return user
        raise NotFoundRepoError(detail='')

    def get_all(self,
                skip: NonNegativeInt = 0,
                limit: PositiveInt = 100) -> List[UserSchema]:
        return self._users

    def get_by_id(self, user_id: ID) -> UserSchema:
        for user in self._users:
            if user.id == user_id:
                return user
        raise NotFoundRepoError(detail='')

    def get_by_email(self, email: Email) -> UserSchema:
        for user in self._users:
            if user.email.value == email.value:
                return user
        raise NotFoundRepoError(detail='')
