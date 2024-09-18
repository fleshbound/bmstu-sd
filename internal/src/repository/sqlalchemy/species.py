import inspect
from contextlib import AbstractContextManager
from typing import List, Callable, cast

from psycopg2.errors import UniqueViolation
from pydantic import NonNegativeInt, BaseModel
from sqlalchemy import insert, update, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.species.repository.species import ISpeciesRepository
from core.species.schema.species import SpeciesSchema
from core.utils import types
from core.utils.exceptions import DuplicatedRepoError, NotFoundRepoError, ValidationRepoError
from repository.sqlalchemy.model.species import SpeciesORM


class SqlAlchemySpeciesRepository(ISpeciesRepository):
    session_factory: Callable[..., AbstractContextManager[Session]]

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def get_all(self, skip: int = 0, limit: int = 100) -> List[SpeciesSchema]:
        with self.session_factory() as session:
            query = select(SpeciesORM).offset(skip).limit(limit)
            rows = session.execute(query).scalars().all()
            return [SpeciesSchema.model_validate(row.to_schema(), from_attributes=True) for row in rows]

    def get_by_id(self, id: NonNegativeInt) -> SpeciesSchema:
        with self.session_factory() as session:
            query = select(SpeciesORM).filter_by(id=id)
            row = session.execute(query).scalar()
            if row is None:
                raise NotFoundRepoError(detail=f"not found id : {id}")
            return SpeciesSchema.model_validate(row.to_schema(), from_attributes=True)

    def create(self, other: SpeciesSchema) -> SpeciesSchema:
        with self.session_factory() as session:
            other_dict = self.get_dict(other, exclude=['id'])
            stmt = insert(SpeciesORM).values(other_dict).returning(SpeciesORM.id)
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
        for field in other.model_fields.keys():
            field_value = getattr(other, field)
            if exclude is None or field not in exclude:
                if type(field_value).__name__ in tuple(x[0] for x in inspect.getmembers(types, inspect.isclass)):
                    # if getattr(field_value, '__module__', None) == types.__name__:
                    #     f = fields(field_value)[0]
                    val = getattr(field_value, 'value')
                    dct[field] = val
                else:
                    dct[field] = field_value
        return dct

    def update(self, other: SpeciesSchema) -> SpeciesSchema:
        with self.session_factory() as session:
            other_dict = self.get_dict(other, exclude=['id'])
            stmt = update(SpeciesORM).where(cast("ColumnElement[bool]", other.id.eq_int(SpeciesORM.id))).values(
                other_dict).returning(SpeciesORM.id)
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
            query = select(SpeciesORM).filter_by(id=id)
            row = session.execute(query).scalar()
            if row is None:
                raise NotFoundRepoError(detail=f"not found id : {id}")
            session.delete(row)
            session.commit()

    def get_by_group_id(self, group_id: NonNegativeInt) -> List[SpeciesSchema]:
        with self.session_factory() as session:
            query = select(SpeciesORM).filter_by(group_id=group_id)
            res = session.execute(query).scalars().all()
            if len(res) == 0:
                raise NotFoundRepoError(detail=f"not found by group_id: {group_id}")
            return [SpeciesSchema.model_validate(row.to_schema(), from_attributes=True) for row in res]
