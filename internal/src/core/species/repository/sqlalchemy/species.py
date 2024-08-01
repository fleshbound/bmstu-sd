from contextlib import AbstractContextManager
from typing import List, Callable

from pydantic import NonNegativeInt
from sqlalchemy.orm import Session

from core.species.schema.species import SpeciesSchema
from database.model.species import SpeciesORM
from utils.exceptions import NotFoundError
from utils.repository.sqlalchemy.base import SqlAlchemyBaseRepository


class SqlAlchemySpeciesRepository(SqlAlchemyBaseRepository):
    session_factory: Callable[..., AbstractContextManager[Session]]

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, SpeciesORM, SpeciesSchema)

    def get_by_group_id(self, group_id: NonNegativeInt) -> List[SpeciesSchema]:
        with self.session_factory() as session:
            res = session.query(self.model).filter_by(group_id=group_id).all()
            if res is None:
                raise NotFoundError(detail=f"not found by group_id : {group_id}")
            return [self.model.to_schema(row) for row in res]
