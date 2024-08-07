from pydantic import NonNegativeInt
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from core.certificate.schema.certificate import CertificateSchema
from database.sqlalchemy.database import Base
from utils.types import ID


class CertificateORM(Base):
    __tablename__ = "certificate"

    id: Mapped[NonNegativeInt] = mapped_column(primary_key=True)
    animalshow_id: Mapped[NonNegativeInt] = mapped_column(ForeignKey(column='animalshow.id'), nullable=False)
    rank: Mapped[NonNegativeInt] = mapped_column(Integer, nullable=False)

    def to_schema(self) -> CertificateSchema:
        return CertificateSchema(
            id=ID(self.id),
            animalshow_id=ID(self.animalshow_id),
            rank=self.rank
        )
