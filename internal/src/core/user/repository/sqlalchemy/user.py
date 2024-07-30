from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from core.user.repository.user import IUserRepository
from core.user.schema.user import UserSchema
from database.model.user import UserORM
from utils.repository.sqlalchemy.base import SqlAlchemyBaseRepository


class SqlAlchemyUserRepository(IUserRepository, SqlAlchemyBaseRepository):
    session_factory: Callable[..., AbstractContextManager[Session]]

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, UserORM, UserSchema)
