from typing import List

from pydantic import NonNegativeInt

from core.species.repository.species import ISpeciesRepository
from core.species.schema.species import SpeciesSchema


class MockedSpeciesRepository(ISpeciesRepository):
    _species: List[SpeciesSchema]

    def __init__(self, speciess: List[SpeciesSchema]):
        self._species = speciess

    def get_by_group_id(self, species_id: NonNegativeInt) -> List[SpeciesSchema]:
        return self._species

    def get_all(self, skip: int = 0, limit: int = 100) -> List[SpeciesSchema]:
        return self._species

    def get_by_id(self, id: NonNegativeInt) -> SpeciesSchema:
        return self._species[0]

    def create(self, object: SpeciesSchema) -> SpeciesSchema:
        self._species.append(object)
        return object

    def update(self, object: SpeciesSchema) -> SpeciesSchema:
        return object

    def delete(self, id: NonNegativeInt) -> None:
        return None
