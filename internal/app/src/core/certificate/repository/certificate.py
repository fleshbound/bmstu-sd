from abc import abstractmethod, ABC
from typing import List

from pydantic import NonNegativeInt

from internal.src.core.certificate.schema.certificate import CertificateSchema


class ICertificateRepository(ABC):
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[CertificateSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: NonNegativeInt) -> CertificateSchema:
        raise NotImplementedError

    @abstractmethod
    def create(self, object: CertificateSchema) -> CertificateSchema:
        raise NotImplementedError

    @abstractmethod
    def update(self, object: CertificateSchema) -> CertificateSchema:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: NonNegativeInt) -> None:
        raise NotImplementedError
