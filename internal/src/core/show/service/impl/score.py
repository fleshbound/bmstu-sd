from collections import OrderedDict
from typing import List, Optional, Tuple

from pydantic import NonNegativeInt, NonNegativeFloat

from core.show.repository.animalshow import IAnimalShowRepository
from core.show.repository.score import IScoreRepository
from core.show.repository.usershow import IUserShowRepository
from core.show.schema.score import TotalScoreInfo, ScoreSchema, ScoreSchemaCreate, ScoreSchemaUpdate, Score, ScoreValue, \
    AniShowRankingInfo
from core.show.service.score import IScoreService
from core.show.service.show import IShowService
from repository.utils.dict.impl.float import FloatKeyDictionary
from core.utils.types import ID


class ScoreService(IScoreService):
    show_service: IShowService
    score_repo: IScoreRepository
    animalshow_repo: IAnimalShowRepository
    usershow_repo: IUserShowRepository

    def __init__(self,
                 show_service: IShowService,
                 score_repo: IScoreRepository,
                 animalshow_repo: IAnimalShowRepository,
                 usershow_repo: IUserShowRepository):
        self.show_service = show_service
        self.score_repo = score_repo
        self.animalshow_repo = animalshow_repo
        self.usershow_repo = usershow_repo

    @staticmethod
    def dict_to_asc_ranked_ids(dict: FloatKeyDictionary) -> List[NonNegativeInt]:
        return list(OrderedDict(sorted(dict.items())).values())

    def get_show_ranking_info(self, show_id: ID) -> Tuple[NonNegativeInt, List[AniShowRankingInfo]]:
        anishow_records = self.animalshow_repo.get_by_show_id(show_id)
        total = []
        for record in anishow_records:
            score_info = self.get_total_by_animalshow_id(record.id)
            total.append(score_info)

        map = FloatKeyDictionary(4)
        for i, res in enumerate(total):
            key = res.average
            if key in map:
                map[key].append(i)
            else:
                map[key] = [i]
        ranked_total_ids = self.dict_to_asc_ranked_ids(map)

        res = []
        for rank, total_id_list in enumerate(ranked_total_ids):
            for total_id in total_id_list:
                info = AniShowRankingInfo(total_info=total[total_id], rank=rank)
                res.append(info)
        return len(ranked_total_ids), res

    def get_total_by_animalshow_id(self, animalshow_id: ID) -> TotalScoreInfo:
        scores = self.score_repo.get_by_animalshow_id(animalshow_id)
        return self.calc_total(animalshow_id, scores)

    def get_total_by_usershow_id(self, usershow_id: ID) -> TotalScoreInfo:
        scores = self.score_repo.get_by_usershow_id(usershow_id)
        return self.calc_total(usershow_id, scores)

    def get_count_by_usershow_id(self, usershow_id: ID) -> NonNegativeInt:
        scores = self.score_repo.get_by_usershow_id(usershow_id)
        return len(scores)

    @staticmethod
    def calc_total(id: ID, scores: List[ScoreSchema]) -> TotalScoreInfo:
        count: NonNegativeInt = len(scores)
        total: Score = Score(0)
        avg: Optional[NonNegativeFloat] = None
        min_score: Optional[ScoreValue] = None
        max_score: Optional[ScoreValue] = None

        if count > 0:
            max_score = ScoreValue(scores[0].value.min)
            min_score = ScoreValue(scores[0].value.max)
            for score in scores:
                cur_score = Score.from_scorevalue(score.value)
                total += cur_score
                if cur_score > max_score:
                    max_score = cur_score
                if cur_score < min_score:
                    min_score = cur_score
            avg = total.value / count

        return TotalScoreInfo(
            record_id=id,
            total=total,
            count=count,
            average=avg,
            min_score=min_score,
            max_score=max_score
        )

    def all_users_scored(self, show_id: ID) -> bool:
        usershows = self.usershow_repo.get_by_show_id(show_id)
        show_animal_count = len(self.show_service.get_by_id_detailed_animals().animals)
        for us in usershows:
            if self.get_count_by_usershow_id(us.id) != show_animal_count:
                return False
        return True

    def get_users_scored_count(self, show_id: ID) -> NonNegativeInt:
        usershows = self.usershow_repo.get_by_show_id(show_id)
        show_animal_count = len(self.show_service.get_by_id_detailed_animals().animals)
        count = 0
        for us in usershows:
            if self.get_count_by_usershow_id(us.id) == show_animal_count:
                count += 1
        return count

    def create(self, score_create: ScoreSchemaCreate) -> ScoreSchema:
        new_score = ScoreSchema.from_create(score_create)
        new_score = self.score_repo.create(new_score)

        cur_show_id = self.usershow_repo.get_by_id(new_score.usershow_id.value).show_id
        if self.all_users_scored(cur_show_id):
            self.show_service.stop(cur_show_id)

        return new_score

    def archive(self, id: ID) -> ScoreSchema:
        update_score_param = ScoreSchemaUpdate(id=id, is_archived=True)
        cur_score = self.score_repo.get_by_id(id)
        new_score = ScoreSchema.from_update(cur_score, update_score_param)
        self.score_repo.update(new_score)
        return new_score

    def get_by_id(self, id: ID) -> ScoreSchema:
        return self.score_repo.get_by_id(id)
