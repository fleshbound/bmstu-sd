import logging
from typing import List

from pydantic import NonNegativeInt, PositiveInt

from core.species.repository.species import ISpeciesRepository
from core.species.schema.species import SpeciesSchema, SpeciesSchemaCreate, SpeciesSchemaUpdate, \
    SpeciesSchemaDelete
from core.species.service.species import ISpeciesService
from core.utils.types import ID


class SpeciesService(ISpeciesService):
    species_repo: ISpeciesRepository

    def __init__(self,
                 species_repo: ISpeciesRepository):
        self.species_repo = species_repo

    def delete(self,
               species_id: ID) -> SpeciesSchemaDelete:
        logging.info(f'delete species id={species_id.value}')
        self.species_repo.delete(species_id.value)
        return SpeciesSchemaDelete(id=species_id)

    def create(self,
               create_species: SpeciesSchemaCreate) -> SpeciesSchema:
        logging.info(f'create species')
        cur_species = SpeciesSchema.from_create(create_species)
        return self.species_repo.create(cur_species)

    def update(self,
               update_species: SpeciesSchemaUpdate) -> SpeciesSchema:
        logging.info(f'update species id={update_species.id.value}')
        cur_species = self.species_repo.get_by_id(update_species.id.value)
        cur_species = cur_species.from_update(update_species)
        return self.species_repo.update(cur_species)

    def get_all(self,
                skip: NonNegativeInt = 0,
                limit: PositiveInt = 100) -> List[SpeciesSchema]:
        logging.info(f'get all species, skip={skip} limit={limit}')
        return self.species_repo.get_all(skip, limit)

    def get_by_group_id(self,
                        group_id: ID) -> List[SpeciesSchema]:
        logging.info(f'get species by group_id={group_id.value}')
        return self.species_repo.get_by_group_id(group_id.value)

    def get_by_id(self, species_id: ID) -> SpeciesSchema:
        logging.info(f'get species by id={species_id.value}')
        return self.species_repo.get_by_id(species_id.value)
