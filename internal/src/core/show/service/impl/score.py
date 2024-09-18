from typing import List, Optional, Tuple

from pydantic import NonNegativeInt, NonNegativeFloat

from core.animal.schema.animal import AnimalSchema
from core.animal.service.animal import IAnimalService
from core.show.repository.score import IScoreRepository
from core.show.schema.score import TotalScoreInfo, ScoreSchema, ScoreSchemaCreate, ScoreSchemaUpdate, \
    AnimalShowRankingInfo
from core.show.service.animalshow import IAnimalShowService
from core.show.service.score import IScoreService
from core.show.service.show import IShowService
from core.show.service.usershow import IUserShowService
from core.utils.dict.impl.float import FloatKeyDictionary
from core.utils.exceptions import ScoreServiceError, NotFoundRepoError
from core.utils.types import ID, Score

DECIMALS = 4


class ScoreService(IScoreService):
    animal_service: IAnimalService
    score_repo: IScoreRepository
    animalshow_service: IAnimalShowService
    usershow_service: IUserShowService

    def __init__(self,
                 animal_service: IAnimalService,
                 score_repo: IScoreRepository,
                 animalshow_service: IAnimalShowService,
                 usershow_service: IUserShowService):
        self.score_repo = score_repo
        self.animal_service = animal_service
        self.animalshow_service = animalshow_service
        self.usershow_service = usershow_service

    @staticmethod
    def dict_to_asc_ranked_ids(dict: FloatKeyDictionary) -> List[NonNegativeInt]:
        avgs = list(dict.keys())
        avgs.sort(reverse=True)
        return [dict[i] for i in avgs]
        # return list(OrderedDict(sorted(dict.keys())).values())

    def get_show_ranking_info(self, show_id: ID) -> Tuple[NonNegativeInt, List[AnimalShowRankingInfo]]:
        animalshow_records = self.animalshow_service.get_by_show_id(show_id)
        total_scores_by_animal = [self.get_total_by_animalshow_id(record.id) for record in animalshow_records]
        total_scores_ranked = self.get_total_scores_ranked(total_scores_by_animal)
        res = []
        for rank, total_id_list in enumerate(total_scores_ranked):
            for total_id in total_id_list:
                res.append(AnimalShowRankingInfo(total_info=total_scores_by_animal[total_id], rank=rank + 1))
        return len(total_scores_ranked), res

    def get_total_scores_ranked(self, total: List[TotalScoreInfo]):
        map = FloatKeyDictionary(DECIMALS)
        for i, res in enumerate(total):
            key = res.average
            if key in map:
                map[key].append(i)
            else:
                map[key] = [i]
        return self.dict_to_asc_ranked_ids(map)

    def get_total_by_animalshow_id(self, animalshow_id: ID) -> TotalScoreInfo:
        try:
            scores = self.score_repo.get_by_animalshow_id(animalshow_id.value)
        except NotFoundRepoError:
            raise ScoreServiceError('no animalshow scores found')
        return self.calc_total(animalshow_id, scores)

    def get_total_by_usershow_id(self, usershow_id: ID) -> TotalScoreInfo:
        try:
            scores = self.score_repo.get_by_usershow_id(usershow_id.value)
        except NotFoundRepoError:
            raise ScoreServiceError('no usershow scores found')
        return self.calc_total(usershow_id, scores)

    def get_count_by_usershow_id(self, usershow_id: ID) -> NonNegativeInt:
        try:
            scores = self.score_repo.get_by_usershow_id(usershow_id.value)
        except NotFoundRepoError:
            raise ScoreServiceError('no usershow scores found')
        return len(scores)

    @staticmethod
    def calc_total(id: ID, scores: List[ScoreSchema]) -> TotalScoreInfo:
        count: NonNegativeInt = len(scores)
        if count == 0:
            raise ScoreServiceError('no scores were given')
        total: Score = Score(0)
        avg: Optional[NonNegativeFloat]
        min_score: Optional[Score]
        max_score: Optional[Score]

        max_score = Score(scores[0].value.min)
        min_score = Score(scores[0].value.max)
        for score in scores:
            cur_score = Score.from_scorevalue(score.value)
            total += cur_score
            if cur_score > max_score:
                max_score = cur_score
            if cur_score < min_score:
                min_score = cur_score
        avg = total.value / count

        return TotalScoreInfo(record_id=id, total=total, count=count, average=avg,
                              min_score=min_score, max_score=max_score)

    def get_animals_by_show_id(self, show_id: ID) -> List[AnimalSchema]:
        animalshow_records = self.animalshow_service.get_by_show_id(show_id)
        animals = []
        for record in animalshow_records:
            animals.append(self.animal_service.get_by_id(record.animal_id))
        return animals

    def all_users_scored(self, show_id: ID) -> bool:
        usershows = self.usershow_service.get_by_show_id(show_id)
        show_animal_count = len(self.get_animals_by_show_id(show_id))
        for us in usershows:
            if self.get_count_by_usershow_id(us.id) != show_animal_count:
                return False
        return True

    def get_users_scored_count(self, show_id: ID) -> NonNegativeInt:
        usershows = self.usershow_service.get_by_show_id(show_id)
        show_animal_count = len(self.get_animals_by_show_id(show_id))
        count = 0
        for us in usershows:
            if self.get_count_by_usershow_id(us.id) == show_animal_count:
                count += 1
        return count

    def create(self, score_create: ScoreSchemaCreate) -> ScoreSchema:
        new_score = ScoreSchema.from_create(score_create)
        new_score = self.score_repo.create(new_score)

        return new_score

    def archive(self, id: ID) -> ScoreSchema:
        update_score_param = ScoreSchemaUpdate(id=id, is_archived=True)
        cur_score = self.score_repo.get_by_id(id.value)
        new_score = ScoreSchema.from_update(cur_score, update_score_param)
        self.score_repo.update(new_score)
        return new_score

    def get_by_id(self, id: ID) -> ScoreSchema:
        return self.score_repo.get_by_id(id.value)
