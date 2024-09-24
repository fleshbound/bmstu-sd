from pydantic import BaseModel, Field

from core.certificate.schema.certificate import CertificateSchema
from core.utils.types import ID
from repository.utils.types import PyObjectId, int_from_pyobject_id


class CertificateORM(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    animalshow_id: int
    rank: int

    def to_schema(self) -> CertificateSchema:
        return CertificateSchema(
            id=ID(int_from_pyobject_id(self.id)),
            animalshow_id=ID(self.animalshow_id),
            rank=self.rank
        )
