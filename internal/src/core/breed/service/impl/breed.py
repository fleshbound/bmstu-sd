from typing import List

from pydantic import NonNegativeInt, PositiveInt

from core.breed.repository.breed import IBreedRepository
from core.breed.schema.breed import BreedSchema, BreedSchemaCreate, BreedSchemaUpdate, BreedSchemaDelete
from core.breed.service.breed import IBreedService
from utils.types import ID


class BreedService(IBreedService):
    breed_repo: IBreedRepository

    def __init__(self,
                 breed_repo: IBreedRepository):
        self.breed_repo = breed_repo

    def delete(self,
               breed_id: ID) -> BreedSchemaDelete:
        self.breed_repo.delete(breed_id.value)
        return BreedSchemaDelete(id=breed_id)

    def create(self,
               create_breed: BreedSchemaCreate) -> BreedSchema:
        return self.breed_repo.create(create_breed)

    def update(self,
               update_breed: BreedSchemaUpdate) -> BreedSchema:
        return self.breed_repo.update(update_breed)

    def get_all(self,
                skip: NonNegativeInt = 0,
                limit: PositiveInt = 100) -> List[BreedSchema]:
        return self.breed_repo.get_all(skip, limit)

    def get_by_species_id(self,
                          species_id: ID) -> List[BreedSchema]:
        return self.breed_repo.get_by_species_id(species_id.value)

    def get_by_id(self, breed_id: ID) -> BreedSchema:
        return self.breed_repo.get_by_id(breed_id.value)
