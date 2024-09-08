from typing import List

from pydantic import NonNegativeInt, PositiveInt

from internal.src.core.certificate.schema.certificate import CertificateSchema, CertificateSchemaCreate
from internal.src.core.certificate.service.certificate import ICertificateService
from internal.src.core.utils.exceptions import NotFoundRepoError
from internal.src.core.utils.types import ID


class MockedCertificateService(ICertificateService):
    _certificates: List[CertificateSchema]
    
    def __init__(self, certificates: List[CertificateSchema]):
        self._certificates = certificates

    def create(self, cert_create: CertificateSchemaCreate) -> CertificateSchema:
        self._certificates.append(CertificateSchema.from_create(cert_create))
        if len(self._certificates) > 0:
            self._certificates[-1].id = ID(len(self._certificates) - 1)
        else:
            self._certificates[-1].id = ID(0)
        return self._certificates[-1]

    def get_by_id(self, cert_id: ID) -> CertificateSchema:
        for cert in self._certificates:
            if cert.id == cert_id:
                return cert
        raise NotFoundRepoError(detail='')

    def get_all(self, skip: NonNegativeInt = 0, limit: PositiveInt = 100) -> List[CertificateSchema]:
        return self._certificates
    