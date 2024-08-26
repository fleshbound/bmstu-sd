from typing import List

from pydantic import NonNegativeInt, PositiveInt

from internal.src.core.breed.repository.breed import IBreedRepository
from internal.src.core.breed.schema.breed import BreedSchema, BreedSchemaCreate, BreedSchemaUpdate, BreedSchemaDelete
from internal.src.core.breed.service.breed import IBreedService
from internal.src.core.utils.types import ID


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
        new_breed = BreedSchema.from_create(create_breed)
        return self.breed_repo.create(new_breed)

    def update(self,
               update_breed: BreedSchemaUpdate) -> BreedSchema:
        cur_breed = self.breed_repo.get_by_id(update_breed.id.value)
        cur_breed.name = update_breed.name
        return self.breed_repo.update(cur_breed)

    def get_all(self,
                skip: NonNegativeInt = 0,
                limit: PositiveInt = 100) -> List[BreedSchema]:
        return self.breed_repo.get_all(skip, limit)

    def get_by_species_id(self,
                          species_id: ID) -> List[BreedSchema]:
        return self.breed_repo.get_by_species_id(species_id.value)

    def get_by_id(self, breed_id: ID) -> BreedSchema:
        return self.breed_repo.get_by_id(breed_id.value)
