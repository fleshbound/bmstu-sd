import inspect
from contextlib import AbstractContextManager
from typing import Callable, Type, List, cast

from psycopg2.errors import UniqueViolation
from pydantic import NonNegativeInt, BaseModel
from sqlalchemy import insert, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.user.repository.user import IUserRepository
from core.user.schema.user import UserSchema
from repository.sqlalchemy.model.user import UserORM
from core.utils import types
from core.utils.exceptions import DuplicatedRepoError, NotFoundRepoError, ValidationRepoError


class SqlAlchemyUserRepository(IUserRepository):
    session_factory: Callable[..., AbstractContextManager[Session]]
    model = Type[UserORM]
    schema = Type[UserSchema]

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def get_all(self, skip: int = 0, limit: int = 100) -> List[UserSchema]:
        with self.session_factory() as session:
            rows = session.query(self.model).offset(skip).limit(limit).all()
            return [self.model.to_schema() for row in rows]

    def get_by_id(self, id: NonNegativeInt) -> UserSchema:
        with self.session_factory() as session:
            row = session.query(self.model).filter_by(id=id).first()
            if row is None:
                raise NotFoundRepoError(detail=f"not found id : {id}")
            return self.model.to_schema()

    def create(self, other: UserSchema) -> UserSchema:
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

    def update(self, other: UserSchema) -> UserSchema:
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

    def get_by_email(self, email: str) -> UserSchema:
        with self.session_factory() as session:
            row = session.query(self.model).filter_by(email=email).first()
            if row is None:
                raise NotFoundRepoError(detail=f"not found email : {email}")
            return self.model.to_schema()
