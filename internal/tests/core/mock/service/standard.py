from typing import List

from pydantic import NonNegativeInt, PositiveInt

from internal.src.core.animal.schema.animal import AnimalSchema
from internal.src.core.standard.schema.standard import StandardSchema, StandardSchemaCreate, \
    StandardSchemaDeleteResponse
from internal.src.core.standard.service.standard import IStandardService
from internal.src.core.utils.exceptions import NotFoundRepoError, CheckAnimalStandardError
from internal.src.core.utils.types import ID


class MockedStandardService(IStandardService):
    _standards: List[StandardSchema]
    
    def __init__(self, standards: List[StandardSchema]):
        self._standards = standards
        
    def get_by_breed_id(self, breed_id: ID) -> List[StandardSchema]:
        return self._standards

    def get_all(self, skip: NonNegativeInt = 0, limit: PositiveInt = 100) -> List[StandardSchema]:
        return self._standards

    def get_by_id(self, id: ID) -> StandardSchema:
        for standard in self._standards:
            if standard.id == id:
                return standard
        raise NotFoundRepoError(detail='')

    def create(self, standard_create: StandardSchemaCreate) -> StandardSchema:
        self._standards.append(StandardSchema.from_create(standard_create))
        if len(self._standards) > 0:
            self._standards[-1].id = ID(len(self._standards) - 1)
        else:
            self._standards[-1].id = ID(0)
        return self._standards[-1]

    def delete(self, id: ID) -> StandardSchemaDeleteResponse:
        for i, record in enumerate(self._standards):
            if record.id == id:
                self._standards.pop(i)
                return StandardSchemaDeleteResponse(id=id)
        return StandardSchemaDeleteResponse(id=id)

    def check_animal_by_standard(self, standard_id: ID, animal: AnimalSchema):
        if standard_id.value / 2:
            raise CheckAnimalStandardError(animal_id=animal.id, standard_id=standard_id)
    