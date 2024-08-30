from abc import ABC, abstractmethod
from typing import List

from pydantic import NonNegativeInt, PositiveInt

from internal.src.core.certificate.schema.certificate import CertificateSchemaCreate, CertificateSchema
from internal.src.core.utils.types import ID


class ICertificateService(ABC):
    @abstractmethod
    def create(self, cert_create: CertificateSchemaCreate) -> CertificateSchema:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, cert_id: ID) -> CertificateSchema:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, skip: NonNegativeInt = 0, limit: PositiveInt = 100) -> List[CertificateSchema]:
        raise NotImplementedError
