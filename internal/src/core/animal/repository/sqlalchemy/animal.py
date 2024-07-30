from contextlib import AbstractContextManager
from typing import Callable, List

from pydantic import NonNegativeInt
from sqlalchemy.orm import Session

from core.animal.repository.animal import IAnimalRepository
from core.animal.schema.animal import AnimalSchema
from database.model.animal import AnimalORM
from utils.exceptions import NotFoundError
from utils.repository.sqlalchemy.base import SqlAlchemyBaseRepository
from utils.types import ID


class SqlAlchemyAnimalRepository(SqlAlchemyBaseRepository, IAnimalRepository):
    session_factory: Callable[..., AbstractContextManager[Session]]

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, AnimalORM, AnimalSchema)

    def get_by_user_id(self, user_id: NonNegativeInt) -> List[AnimalSchema]:
        with self.session_factory() as session:
            res = session.query(self.model).filter_by(user_id=user_id).all()
            if res is None:
                raise NotFoundError(detail=f"not found by user_id : {user_id}")
            return [self.model.to_schema(row) for row in res]
