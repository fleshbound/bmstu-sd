import inspect
from contextlib import AbstractContextManager
from typing import Callable, List, Type, cast

from psycopg2.errors import UniqueViolation
from pydantic import NonNegativeInt, BaseModel
from sqlalchemy import update, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from internal.src.core.show.repository.score import IScoreRepository
from internal.src.core.show.schema.score import ScoreSchema
from internal.src.core.utils import types
from internal.src.core.utils.exceptions import NotFoundRepoError, DuplicatedRepoError, ValidationRepoError
from internal.src.repository.sqlalchemy.model.score import ScoreORM


class SqlAlchemyScoreRepository(IScoreRepository):
    session_factory: Callable[..., AbstractContextManager[Session]]
    model = Type[ScoreORM]
    schema = Type[ScoreSchema]

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ScoreSchema]:
        with self.session_factory() as session:
            rows = session.query(self.model).offset(skip).limit(limit).all()
            return [self.model.to_schema() for row in rows]

    def get_by_id(self, id: NonNegativeInt) -> ScoreSchema:
        with self.session_factory() as session:
            row = session.query(self.model).filter_by(id=id).first()
            if row is None:
                raise NotFoundRepoError(detail=f"not found id : {id}")
            return self.model.to_schema()

    def get_by_animalshow_id(self, animalshow_id: NonNegativeInt) -> List[ScoreSchema]:
        with self.session_factory() as session:
            res = session.query(self.model).filter_by(animalshow_id=animalshow_id).all()
            if res is None:
                raise NotFoundRepoError(detail=f"not found by animalshow_id : {animalshow_id}")
            return [self.model.to_schema() for row in res]

    def get_by_usershow_id(self, usershow_id: NonNegativeInt) -> List[ScoreSchema]:
        with self.session_factory() as session:
            res = session.query(self.model).filter_by(usershow_id=usershow_id).all()
            if res is None:
                raise NotFoundRepoError(detail=f"not found by usershow_id : {usershow_id}")
            return [self.model.to_schema() for row in res]

    def create(self, other: ScoreSchema) -> ScoreSchema:
        with self.session_factory() as session:
            other_dict = self.get_dict(other)
            stmt = insert(self.model).values(other_dict).returning(self.model.id)
            try:
                result = session.execute(stmt)
                session.commit()
            except IntegrityError as e:
                if isinstance(e.orig, UniqueViolation):
                    raise DuplicatedRepoError(detail=str(e.orig))
                raise ValidationRepoError(detail=str(e.orig))
            row = result.fetchone()
            return self.get_by_id(row[0])

    @staticmethod
    def get_dict(other: BaseModel, exclude: List[str] | None = None) -> dict:
        dct = dict()
        for field in other.__fields__.keys():
            field_value = getattr(other, field)
            if exclude is None or field not in exclude:
                if type(field_value).__name__ in tuple(x[0] for x in inspect.getmembers(types, inspect.isclass)):
                    val = getattr(field_value, 'value')
                    dct[field] = val
                else:
                    dct[field] = field_value
        return dct

    def update(self, other: ScoreSchema) -> ScoreSchema:
        with self.session_factory() as session:
            other_dict = self.get_dict(other, exclude=['id'])
            stmt = update(self.model
                          ).where(cast("ColumnElement[bool]", other.id.eq_int(self.model.id))
                                  ).values(other_dict
                                           ).returning(self.model.id)
            try:
                result = session.execute(stmt)
                session.commit()
            except IntegrityError as e:
                if isinstance(e.orig, UniqueViolation):
                    raise DuplicatedRepoError(detail=str(e.orig))
                raise ValidationRepoError(detail=str(e.orig))
            row = result.fetchone()
            if row is None:
                raise NotFoundRepoError(detail=f"not found id : {id}")

            return self.get_by_id(row[0])

    def delete(self, id: NonNegativeInt) -> None:
        with self.session_factory() as session:
            row = session.query(self.model).filter_by(id=id).first()
            if row is None:
                raise NotFoundRepoError(detail=f"not found id : {id}")
            session.delete(row)
            session.commit()
    