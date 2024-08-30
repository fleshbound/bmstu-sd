from typing import List

from pydantic import NonNegativeInt

from internal.src.core.standard.repository.standard import IStandardRepository
from internal.src.core.standard.schema.standard import StandardSchema


class MockedStandardRepository(IStandardRepository):
    _standards: List[StandardSchema]

    def __init__(self, standards: List[StandardSchema]):
        self._standards = standards

    def get_by_breed_id(self, user_id: NonNegativeInt) -> List[StandardSchema]:
        return self._standards

    def get_all(self, skip: int = 0, limit: int = 100) -> List[StandardSchema]:
        return self._standards

    def get_by_id(self, id: NonNegativeInt) -> StandardSchema:
        return self._standards[0]

    def create(self, other: StandardSchema) -> StandardSchema:
        return other

    def update(self, other: StandardSchema) -> StandardSchema:
        return other

    def delete(self, id: NonNegativeInt) -> None:
        return None
