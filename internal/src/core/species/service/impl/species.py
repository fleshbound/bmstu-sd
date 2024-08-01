from typing import List

from pydantic import NonNegativeInt, PositiveInt

from core.species.repository.species import ISpeciesRepository
from core.species.schema.species import SpeciesSchema, SpeciesSchemaCreate, SpeciesSchemaUpdate, SpeciesSchemaDelete
from core.species.service.species import ISpeciesService
from utils.types import ID


class SpeciesService(ISpeciesService):
    species_repo: ISpeciesRepository

    def __init__(self,
                 species_repo: ISpeciesRepository):
        self.species_repo = species_repo

    def delete(self,
               species_id: ID) -> SpeciesSchemaDelete:
        self.species_repo.delete(species_id.value)
        return SpeciesSchemaDelete(id=species_id)

    def create(self,
               create_species: SpeciesSchemaCreate) -> SpeciesSchema:
        return self.species_repo.create(create_species)

    def update(self,
               update_species: SpeciesSchemaUpdate) -> SpeciesSchema:
        return self.species_repo.update(update_species)

    def get_all(self,
                skip: NonNegativeInt = 0,
                limit: PositiveInt = 100) -> List[SpeciesSchema]:
        return self.species_repo.get_all(skip, limit)

    def get_by_group_id(self,
                        group_id: ID) -> List[SpeciesSchema]:
        return self.species_repo.get_by_group_id(group_id.value)

    def get_by_id(self, species_id: ID) -> SpeciesSchema:
        return self.species_repo.get_by_id(species_id.value)
