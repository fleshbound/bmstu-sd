from typing import List, Tuple

from pydantic import NonNegativeInt

from internal.src.core.show.schema.score import ScoreSchema, TotalScoreInfo, ScoreSchemaCreate, AnimalShowRankingInfo
from internal.src.core.show.schema.show import ShowSchema
from internal.src.core.show.service.score import IScoreService
from internal.src.core.utils.exceptions import NotFoundRepoError
from internal.src.core.utils.types import ID, Score


class MockedScoreService(IScoreService):
    _scores: List[ScoreSchema]
    _shows: List[ShowSchema]
    
    def __init__(self, scores: List[ScoreSchema]):
        self._scores = scores

    def get_total_by_animalshow_id(self, animalshow_id: ID) -> TotalScoreInfo:
        return TotalScoreInfo(
            record_id=ID(0),
            total=Score(0),
            count=0,
            average=None,
            max_score=None,
            min_score=None
        )

    def get_show_ranking_info(self, show_id: ID) -> Tuple[NonNegativeInt, List[AnimalShowRankingInfo]]:
        return 0, []

    def get_total_by_usershow_id(self, usershow_id: ID) -> TotalScoreInfo:
        return TotalScoreInfo(
            record_id=ID(0),
            total=Score(0),
            count=0,
            average=None,
            max_score=None,
            min_score=None
        )

    def all_users_scored(self, show_id: ID) -> bool:
        return show_id.value / 2 == 0

    def get_users_scored_count(self, show_id: ID) -> NonNegativeInt:
        return 100

    def create(self, score_create: ScoreSchemaCreate) -> ScoreSchema:
        self._scores.append(ScoreSchema.from_create(score_create))
        if len(self._scores) > 0:
            self._scores[-1].id = ID(len(self._scores) - 1)
        else:
            self._scores[-1].id = ID(0)
        return self._scores[-1]

    def archive(self, id: ID) -> ScoreSchema:
        for score in self._scores:
            if score.id == id:
                score.is_archived = True
                return score

    def get_by_id(self, id: ID) -> ScoreSchema:
        for score in self._scores:
            if score.id == id:
                return score
        raise NotFoundRepoError(detail='')
    