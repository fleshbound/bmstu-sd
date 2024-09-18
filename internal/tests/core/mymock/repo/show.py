from typing import List

from pydantic import NonNegativeInt

from core.show.repository.show import IShowRepository
from core.show.schema.show import ShowSchema


class MockedShowRepository(IShowRepository):
    _shows: List[ShowSchema]

    def __init__(self, shows: List[ShowSchema]):
        self._shows = shows

    def get_by_breed_id(self, user_id: NonNegativeInt) -> List[ShowSchema]:
        return self._shows

    def get_by_species_id(self, user_id: NonNegativeInt) -> List[ShowSchema]:
        return self._shows

    def get_by_standard_id(self, user_id: NonNegativeInt) -> List[ShowSchema]:
        return self._shows

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ShowSchema]:
        return self._shows

    def get_by_id(self, id: NonNegativeInt) -> ShowSchema:
        return self._shows[0]

    def create(self, other: ShowSchema) -> ShowSchema:
        return other

    def update(self, other: ShowSchema) -> ShowSchema:
        return other

    def delete(self, id: NonNegativeInt) -> None:
        return None
