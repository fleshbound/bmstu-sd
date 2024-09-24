import logging
from typing import List

from pydantic import NonNegativeInt, PositiveInt

from core.certificate.repository.certificate import ICertificateRepository
from core.certificate.schema.certificate import CertificateSchemaCreate, CertificateSchema
from core.certificate.service.certificate import ICertificateService
from core.utils.types import ID


class CertificateService(ICertificateService):
    certificate_repo: ICertificateRepository

    def __init__(self, certificate_repo: ICertificateRepository):
        self.certificate_repo = certificate_repo

    def create(self, cert_create: CertificateSchemaCreate) -> CertificateSchema:
        logging.info(f'create certificate animalshow_id={cert_create.animalshow_id.value}')
        cert = CertificateSchema.from_create(cert_create)
        return self.certificate_repo.create(cert)

    def get_by_id(self, cert_id: ID) -> CertificateSchema:
        logging.info(f'get certificate by id={cert_id.value}')
        return self.certificate_repo.get_by_id(cert_id.value)

    def get_all(self, skip: NonNegativeInt = 0, limit: PositiveInt = 100) -> List[CertificateSchema]:
        logging.info(f'get all certificates skip={skip}, limit={limit}')
        return self.certificate_repo.get_all(skip, limit)