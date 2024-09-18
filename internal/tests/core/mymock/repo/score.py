from typing import List

from pydantic import NonNegativeInt

from core.show.repository.score import IScoreRepository
from core.show.schema.score import ScoreSchema
from core.utils.exceptions import NotFoundRepoError


class MockedScoreRepository(IScoreRepository):
    _scores: List[ScoreSchema]
    
    def __init__(self, scores: List[ScoreSchema]):
        self._scores = scores
        
    def get_by_animalshow_id(self, animalshow_id: NonNegativeInt) -> List[ScoreSchema]:
        res = []
        for score in self._scores:
            if score.animalshow_id == animalshow_id:
                res.append(score)
        if not len(res):
            raise NotFoundRepoError()
        return res
        
    def get_by_usershow_id(self, usershow_id: NonNegativeInt) -> List[ScoreSchema]:
        res = []
        for score in self._scores:
            if score.usershow_id == usershow_id:
                res.append(score)
        if not len(res):
            raise NotFoundRepoError()
        return res

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ScoreSchema]:
        return self._scores

    def get_by_id(self, id: NonNegativeInt) -> ScoreSchema:
        for score in self._scores:
            if score.id == id:
                return score
        raise NotFoundRepoError()

    def create(self, other: ScoreSchema) -> ScoreSchema:
        return other

    def update(self, other: ScoreSchema) -> ScoreSchema:
        return other

    def delete(self, id: NonNegativeInt) -> None:
        return None
    