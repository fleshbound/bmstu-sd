from typing import List

from pydantic import NonNegativeInt

from internal.src.core.animal.repository.animal import IAnimalRepository
from internal.src.core.animal.schema.animal import AnimalSchema


class MockedAnimalRepository(IAnimalRepository):
    _animals: List[AnimalSchema]

    def __init__(self, animals: List[AnimalSchema]):
        self._animals = animals

    def get_by_user_id(self, user_id: NonNegativeInt) -> List[AnimalSchema]:
        return self._animals

    def get_all(self, skip: int = 0, limit: int = 100) -> List[AnimalSchema]:
        return self._animals

    def get_by_id(self, id: NonNegativeInt) -> AnimalSchema:
        return self._animals[0]

    def create(self, other: AnimalSchema) -> AnimalSchema:
        return other

    def update(self, other: AnimalSchema) -> AnimalSchema:
        return other

    def delete(self, id: NonNegativeInt) -> None:
        return None
