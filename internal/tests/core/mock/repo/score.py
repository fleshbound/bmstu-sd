from typing import List

from pydantic import NonNegativeInt

from internal.src.core.show.repository.score import IScoreRepository
from internal.src.core.show.schema.score import ScoreSchema


class MockedScoreRepository(IScoreRepository):
    _scores: List[ScoreSchema]
    
    def __init__(self, scores: List[ScoreSchema]):
        self._scores = scores
        
    def get_by_animalshow_id(self, animalshow_id: NonNegativeInt) -> List[ScoreSchema]:
        return self._scores
        
    def get_by_usershow_id(self, usershow_id: NonNegativeInt) -> List[ScoreSchema]:
        return self._scores

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ScoreSchema]:
        return self._scores

    def get_by_id(self, id: NonNegativeInt) -> ScoreSchema:
        return self._scores[0]

    def create(self, other: ScoreSchema) -> ScoreSchema:
        return other

    def update(self, other: ScoreSchema) -> ScoreSchema:
        return other

    def delete(self, id: NonNegativeInt) -> None:
        return None
    