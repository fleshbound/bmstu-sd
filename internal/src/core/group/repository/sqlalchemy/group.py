from contextlib import AbstractContextManager
from typing import List, Callable

from pydantic import NonNegativeInt
from sqlalchemy.orm import Session

from core.group.schema.group import GroupSchema
from database.model.group import GroupORM
from utils.exceptions import NotFoundError
from utils.repository.sqlalchemy.base import SqlAlchemyBaseRepository


class SqlAlchemyGroupRepository(SqlAlchemyBaseRepository):
    session_factory: Callable[..., AbstractContextManager[Session]]

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, GroupORM, GroupSchema)
