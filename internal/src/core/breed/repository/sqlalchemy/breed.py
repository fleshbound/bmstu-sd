from contextlib import AbstractContextManager
from typing import List, Callable

from pydantic import NonNegativeInt
from sqlalchemy.orm import Session

from core.breed.schema.breed import BreedSchema
from database.model.breed import BreedORM
from utils.exceptions import NotFoundError
from utils.repository.sqlalchemy.base import SqlAlchemyBaseRepository


class SqlAlchemyBreedRepository(SqlAlchemyBaseRepository):
    session_factory: Callable[..., AbstractContextManager[Session]]

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, BreedORM, BreedSchema)

    def get_by_species_id(self, species_id: NonNegativeInt) -> List[BreedSchema]:
        with self.session_factory() as session:
            res = session.query(self.model).filter_by(species_id=species_id).all()
            if res is None:
                raise NotFoundError(detail=f"not found by species_id : {species_id}")
            return [self.model.to_schema(row) for row in res]
