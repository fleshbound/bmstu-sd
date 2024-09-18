from typing import List, Optional

from pydantic import NonNegativeInt

from core.animal.repository.animal import IAnimalRepository
from core.animal.schema.animal import AnimalSchema


class MockedAnimalRepository(IAnimalRepository):
    _animals: List[AnimalSchema]

    def __init__(self, animals: List[AnimalSchema]):
        self._animals = animals

    def get_by_user_id(self, user_id: NonNegativeInt) -> List[AnimalSchema]:
        return self._animals

    def get_all(self, skip: int = 0, limit: Optional[int] = None) -> List[AnimalSchema]:
        return self._animals

    def get_by_id(self, id: NonNegativeInt) -> AnimalSchema:
        return self._animals[0]

    def create(self, other: AnimalSchema) -> AnimalSchema:
        return other

    def update(self, other: AnimalSchema) -> AnimalSchema:
        return other

    def delete(self, id: NonNegativeInt) -> None:
        return None
