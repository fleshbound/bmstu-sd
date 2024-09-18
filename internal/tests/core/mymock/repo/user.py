from typing import List

from pydantic import NonNegativeInt

from core.breed.repository.breed import IBreedRepository
from core.breed.schema.breed import BreedSchema


class MockedBreedRepository(IBreedRepository):
    _breeds: List[BreedSchema]

    def __init__(self, breeds: List[BreedSchema]):
        self._breeds = breeds

    def get_by_species_id(self, species_id: NonNegativeInt) -> List[BreedSchema]:
        return self._breeds

    def get_all(self, skip: int = 0, limit: int = 100) -> List[BreedSchema]:
        return self._breeds

    def get_by_id(self, id: NonNegativeInt) -> BreedSchema:
        return self._breeds[0]

    def create(self, object: BreedSchema) -> BreedSchema:
        self._breeds.append(object)
        return object

    def update(self, object: BreedSchema) -> BreedSchema:
        return object

    def delete(self, id: NonNegativeInt) -> None:
        return None
