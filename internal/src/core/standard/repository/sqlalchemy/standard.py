import inspect
from contextlib import AbstractContextManager
from typing import List, Callable, Type

from psycopg2.errors import UniqueViolation
from sqlalchemy import IntegrityError
from pydantic import NonNegativeInt, BaseModel
from sqlalchemy import insert
from sqlalchemy.orm import Session

from core.standard.repository.standard import IStandardRepository
from core.standard.schema.standard import StandardSchema, StandardSchemaCreate

from database.sqlalchemy.model.standard import StandardORM
from utils import types
from utils.exceptions import NotFoundRepoError, DuplicatedRepoError, ValidationRepoError


class SqlAlchemyStandardRepository(IStandardRepository):
    session_factory: Callable[..., AbstractContextManager[Session]]
    model = Type[StandardORM]
    schema = Type[StandardSchema]

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def get_by_breed_id(self, breed_id: NonNegativeInt) -> List[StandardSchema]:
        with self.session_factory() as session:
            res = session.query(self.model).filter_by(breed_id=breed_id).all()
            if res is None:
                raise NotFoundRepoError(detail=f"not found by breed_id : {breed_id}")
            return [self.model.to_schema() for row in res]

    def get_all(self, skip: int = 0, limit: int = 100) -> List[StandardSchema]:
        with self.session_factory() as session:
            rows = session.query(self.model).offset(skip).limit(limit).all()
            return [self.model.to_schema() for row in rows]

    def get_by_id(self, id: NonNegativeInt) -> StandardSchema:
        with self.session_factory() as session:
            row = session.query(self.model).filter_by(id=id).first()
            if row is None:
                raise NotFoundRepoError(detail=f"not found id : {id}")
            return self.model.to_schema()

    def create(self, other: StandardSchemaCreate) -> StandardSchema:
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
                if type(field_value).__name__ in tuple(x[0] for x in inspect.getmembers(types,inspect.isclass)):
                    # if getattr(field_value, '__module__', None) == types.__name__:
                    #     f = fields(field_value)[0]
                    val = getattr(field_value, 'value')
                    dct[field] = val
                else:
                    dct[field] = field_value
        return dct

    def delete(self, id: NonNegativeInt) -> None:
        with self.session_factory() as session:
            row = session.query(self.model).filter_by(id=id).first()
            if row is None:
                raise NotFoundRepoError(detail=f"not found id : {id}")
            session.delete(row)
            session.commit()
