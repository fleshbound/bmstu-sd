from pydantic import BaseModel, NonNegativeInt

from internal.src.core.utils.types import ID


class CertificateSchemaCreate(BaseModel):
    animalshow_id: ID
    rank: NonNegativeInt


class CertificateSchema(BaseModel):
    id: ID
    animalshow_id: ID
    rank: NonNegativeInt

    @classmethod
    def from_create(cls, other: CertificateSchemaCreate):
        return cls(
            id=ID(0),
            animalshow_id=other.animalshow_id,
            rank=other.rank
        )
