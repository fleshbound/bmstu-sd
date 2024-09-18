import inspect
from contextlib import AbstractContextManager
from typing import List, Callable, Type, cast, Optional

from psycopg2.errors import UniqueViolation
from pydantic import NonNegativeInt, BaseModel
from sqlalchemy import insert, update, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.certificate.repository.certificate import ICertificateRepository
from core.certificate.schema.certificate import CertificateSchema
from core.utils import types
from core.utils.exceptions import DuplicatedRepoError, NotFoundRepoError, ValidationRepoError
from repository.sqlalchemy.model.certificate import CertificateORM


class SqlAlchemyCertificateRepository(ICertificateRepository):
    session_factory: Callable[..., AbstractContextManager[Session]]
    model = Type[CertificateORM]
    schema = Type[CertificateSchema]

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def get_all(self, skip: int = 0, limit: Optional[int] = None) -> List[CertificateSchema]:
        with self.session_factory() as session:
            if limit is None:
                query = select(CertificateORM).offset(skip)
            else:
                query = select(CertificateORM).offset(skip).limit(limit)
            rows = session.execute(query).scalars().all()
            return [CertificateSchema.model_validate(row.to_schema(), from_attributes=True) for row in rows]

    def get_by_id(self, id: NonNegativeInt) -> CertificateSchema:
        with self.session_factory() as session:
            query = select(CertificateORM).filter_by(id=id)
            row = session.execute(query).scalar()
            if row is None:
                raise NotFoundRepoError(detail=f"not found id : {id}")
            return CertificateSchema.model_validate(row.to_schema(), from_attributes=True)

    def create(self, other: CertificateSchema) -> CertificateSchema:
        with self.session_factory() as session:
            other_dict = self.get_dict(other, exclude=['id'])
            stmt = insert(CertificateORM).values(other_dict).returning(CertificateORM.id)
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
                    val = getattr(field_value, 'value')
                    dct[field] = val
                else:
                    dct[field] = field_value
        return dct

    def update(self, other: CertificateSchema) -> CertificateSchema:
        with self.session_factory() as session:
            other_dict = self.get_dict(other, exclude=['id'])
            stmt = update(CertificateORM).where(cast("ColumnElement[bool]", other.id.eq_int(CertificateORM.id))).values(
                other_dict).returning(CertificateORM.id)
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
            query = select(CertificateORM).filter_by(id=id)
            row = session.execute(query).scalar()
            if row is None:
                raise NotFoundRepoError(detail=f"not found id : {id}")
            session.delete(row)
            session.commit()
