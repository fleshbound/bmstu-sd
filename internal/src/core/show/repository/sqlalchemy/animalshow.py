import inspect
from contextlib import AbstractContextManager
from typing import List, Callable, Type, cast

from psycopg2.errors import UniqueViolation
from pydantic import NonNegativeInt, BaseModel
from sqlalchemy import insert, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.show.repository.animalshow import IAnimalShowRepository
from core.show.schema.animalshow import AnimalShowSchema, AnimalShowSchemaCreate, AnimalShowSchemaUpdate
from database.sqlalchemy.model.animalshow import AnimalShowORM
from utils import types
from utils.exceptions import NotFoundError, DuplicatedError, ValidationError


class SqlAlchemyAnimalShowRepository(IAnimalShowRepository):
    session_factory: Callable[..., AbstractContextManager[Session]]
    model = Type[AnimalShowORM]
    schema = Type[AnimalShowSchema]

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def get_all(self, skip: int = 0, limit: int = 100) -> List[AnimalShowSchema]:
        with self.session_factory() as session:
            rows = session.query(self.model).offset(skip).limit(limit).all()
            return [self.model.to_schema(row) for row in rows]

    def get_by_id(self, id: NonNegativeInt) -> AnimalShowSchema:
        with self.session_factory() as session:
            row = session.query(self.model).filter_by(id=id).first()
            if row is None:
                raise NotFoundError(detail=f"not found id : {id}")
            return self.model.to_schema(row)

    def create(self, other: AnimalShowSchemaCreate) -> AnimalShowSchema:
        with self.session_factory() as session:
            other_dict = self.get_dict(other)
            stmt = insert(self.model).values(other_dict).returning(self.model.id)
            try:
                result = session.execute(stmt)
                session.commit()
            except IntegrityError as e:
                if isinstance(e.orig, UniqueViolation):
                    raise DuplicatedError(detail=str(e.orig))
                raise ValidationError(detail=str(e.orig))
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

    def update(self, other: AnimalShowSchemaUpdate) -> AnimalShowSchema:
        with self.session_factory() as session:
            other_dict = self.get_dict(other, exclude=['id'])
            stmt = update(self.model
                          ).where(cast("ColumnElement[bool]", self.model.id==other.id.value)
                                  ).values(other_dict
                                           ).returning(self.model.id)
            try:
                result = session.execute(stmt)
                session.commit()
            except IntegrityError as e:
                if isinstance(e.orig, UniqueViolation):
                    raise DuplicatedError(detail=str(e.orig))
                raise ValidationError(detail=str(e.orig))
            row = result.fetchone()
            if row is None:
                raise NotFoundError(detail=f"not found id : {id}")

            return self.get_by_id(row[0])

    def delete(self, id: NonNegativeInt) -> None:
        with self.session_factory() as session:
            row = session.query(self.model).filter_by(id=id).first()
            if row is None:
                raise NotFoundError(detail=f"not found id : {id}")
            session.delete(row)
            session.commit()

    def get_by_animal_id(self, animal_id: NonNegativeInt) -> List[AnimalShowSchema]:
        with self.session_factory() as session:
            res = session.query(self.model).filter_by(animal_id=animal_id).all()
            if res is None:
                raise NotFoundError(detail=f"not found animal_id : {animal_id}")
            return [self.model.to_schema(row) for row in res]

    def get_by_show_id(self, show_id: NonNegativeInt) -> List[AnimalShowSchema]:
        with self.session_factory() as session:
            res = session.query(self.model).filter_by(show_id=show_id).all()
            if res is None:
                raise NotFoundError(detail=f"not found show_id : {show_id}")
            return [self.model.to_schema(row) for row in res]
