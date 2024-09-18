from typing import List

from pydantic import NonNegativeInt, PositiveInt

from core.breed.schema.breed import BreedSchema, BreedSchemaDelete, BreedSchemaCreate, BreedSchemaUpdate
from core.breed.service.breed import IBreedService
from core.utils.exceptions import NotFoundRepoError
from core.utils.types import ID


class MockedBreedService(IBreedService):
    _breeds: List[BreedSchema]
    
    def __init__(self, breeds: List[BreedSchema]):
        self._breeds = breeds

    def delete(self,
               breed_id: ID) -> BreedSchemaDelete:
        return BreedSchemaDelete(id=breed_id)

    def create(self,
               create_breed: BreedSchemaCreate) -> BreedSchema:
        self._breeds.append(BreedSchema.from_create(create_breed))
        if len(self._breeds) > 0:
            self._breeds[-1].id = ID(len(self._breeds) - 1)
        else:
            self._breeds[-1].id = ID(0)
        return self._breeds[-1]

    def update(self,
               update_breed: BreedSchemaUpdate) -> BreedSchema:
        for breed in self._breeds:
            if breed.id == update_breed.id:
                breed = breed.from_update(update_breed)
                return breed
        raise NotFoundRepoError(detail='')

    def get_all(self,
                skip: NonNegativeInt = 0,
                limit: PositiveInt = 100) -> List[BreedSchema]:
        return self._breeds

    def get_by_species_id(self,
                          species_id: ID) -> List[BreedSchema]:
        return self._breeds

    def get_by_id(self, breed_id: ID) -> BreedSchema:
        for breed in self._breeds:
            if breed.id == breed_id:
                return breed
        raise NotFoundRepoError(detail='')
    