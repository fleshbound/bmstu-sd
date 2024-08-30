from collections import OrderedDict
from typing import List, Optional, Tuple

from pydantic import NonNegativeInt, NonNegativeFloat
from repository.utils.dict.impl.float import FloatKeyDictionary

<<<<<<< HEAD
<<<<<<< HEAD
from internal.src.core.show.repository.score import IScoreRepository
from internal.src.core.show.service.usershow import IUserShowService
from internal.src.core.show.schema.score import TotalScoreInfo, ScoreSchema, ScoreSchemaCreate, ScoreSchemaUpdate, Score, ScoreValue, \
||||||| parent of d8bdfb9 (add animal tests (init))
from core.show.repository.animalshow import IAnimalShowRepository
from core.show.repository.score import IScoreRepository
from core.show.repository.usershow import IUserShowRepository
from core.show.schema.score import TotalScoreInfo, ScoreSchema, ScoreSchemaCreate, ScoreSchemaUpdate, Score, ScoreValue, \
=======
from internal.src.core.show.repository.animalshow import IAnimalShowRepository
||||||| parent of 0206eae (add score tests files)
from internal.src.core.show.repository.animalshow import IAnimalShowRepository
=======
from internal.src.core.show.repository.animalshow import IAnimalShowService
>>>>>>> 0206eae (add score tests files)
from internal.src.core.show.repository.score import IScoreRepository
from internal.src.core.show.repository.usershow import IUserShowService
from internal.src.core.show.schema.score import TotalScoreInfo, ScoreSchema, ScoreSchemaCreate, ScoreSchemaUpdate, Score, ScoreValue, \
<<<<<<< HEAD
>>>>>>> d8bdfb9 (add animal tests (init))
    AniShowRankingInfo
<<<<<<< HEAD
<<<<<<< HEAD
from internal.src.core.show.service.animalshow import IAnimalShowService
from internal.src.core.show.service.score import IScoreService
from internal.src.core.show.service.show import IShowService
from repository.utils.dict.impl.float import FloatKeyDictionary
from internal.src.core.utils.types import ID
||||||| parent of fb32d3b (tests arent working watahel)
from core.show.service.score import IScoreService
from core.show.service.show import IShowService
from repository.utils.dict.impl.float import FloatKeyDictionary
from core.utils.types import ID
=======
from core.show.service.score import IScoreService
from core.show.service.show import IShowService
from core.utils.types import ID
>>>>>>> fb32d3b (tests arent working watahel)
||||||| parent of d8bdfb9 (add animal tests (init))
from core.show.service.score import IScoreService
from core.show.service.show import IShowService
from core.utils.types import ID
=======
||||||| parent of 1181f99 (add show service tests)
    AniShowRankingInfo
=======
    AnimalShowRankingInfo
>>>>>>> 1181f99 (add show service tests)
from internal.src.core.show.service.score import IScoreService
from internal.src.core.show.service.show import IShowService
from internal.src.core.utils.types import ID
>>>>>>> d8bdfb9 (add animal tests (init))


class ScoreService(IScoreService):
    show_service: IShowService
    score_repo: IScoreRepository
    animalshow_service: IAnimalShowService
    usershow_service: IUserShowService

    def __init__(self,
                 show_service: IShowService,
                 score_repo: IScoreRepository,
<<<<<<< HEAD
                 animalshow_service: IAnimalShowService,
                 usershow_service: IUserShowService):
        self.show_service = show_service
||||||| parent of 0206eae (add score tests files)
                 animalshow_repo: IAnimalShowRepository,
                 usershow_repo: IUserShowRepository):
        self.show_service = show_service
=======
                 animalshow_service: IAnimalShowService,
                 usershow_service: IUserShowService):
>>>>>>> 0206eae (add score tests files)
        self.score_repo = score_repo
<<<<<<< HEAD
        self.animalshow_service = animalshow_service
        self.usershow_service = usershow_service
||||||| parent of 0206eae (add score tests files)
        self.animalshow_repo = animalshow_repo
        self.usershow_repo = usershow_repo
=======
        self.show_service = show_service
        self.animalshow_service = animalshow_service
        self.usershow_service = usershow_service
>>>>>>> 0206eae (add score tests files)

    @staticmethod
    def dict_to_asc_ranked_ids(dict: FloatKeyDictionary) -> List[NonNegativeInt]:
        return list(OrderedDict(sorted(dict.items())).values())

<<<<<<< HEAD
    def get_show_ranking_info(self, show_id: ID) -> Tuple[NonNegativeInt, List[AniShowRankingInfo]]:
        anishow_records = self.animalshow_service.get_by_show_id(show_id)
||||||| parent of 1181f99 (add show service tests)
    def get_show_ranking_info(self, show_id: ID) -> Tuple[NonNegativeInt, List[AniShowRankingInfo]]:
        anishow_records = self.animalshow_repo.get_by_show_id(show_id)
=======
    def get_show_ranking_info(self, show_id: ID) -> Tuple[NonNegativeInt, List[AnimalShowRankingInfo]]:
<<<<<<< HEAD
        anishow_records = self.animalshow_repo.get_by_show_id(show_id)
>>>>>>> 1181f99 (add show service tests)
||||||| parent of 0206eae (add score tests files)
        anishow_records = self.animalshow_repo.get_by_show_id(show_id)
=======
        anishow_records = self.animalshow_service.get_by_show_id(show_id)
>>>>>>> 0206eae (add score tests files)
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
                info = AnimalShowRankingInfo(total_info=total[total_id], rank=rank)
                res.append(info)
        return len(ranked_total_ids), res

    def get_total_by_animalshow_id(self, animalshow_id: ID) -> TotalScoreInfo:
        scores = self.score_repo.get_by_animalshow_id(animalshow_id.value)
        return self.calc_total(animalshow_id, scores)

    def get_total_by_usershow_id(self, usershow_id: ID) -> TotalScoreInfo:
        scores = self.score_repo.get_by_usershow_id(usershow_id.value)
        return self.calc_total(usershow_id, scores)

    def get_count_by_usershow_id(self, usershow_id: ID) -> NonNegativeInt:
        scores = self.score_repo.get_by_usershow_id(usershow_id.value)
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
<<<<<<< HEAD
<<<<<<< HEAD
        usershows = self.usershow_service.get_by_show_id(show_id)
        show_animal_count = len(self.show_service.get_by_id_detailed(show_id).animals)
||||||| parent of 1181f99 (add show service tests)
        usershows = self.usershow_repo.get_by_show_id(show_id)
        show_animal_count = len(self.show_service.get_by_id_detailed_animals().animals)
=======
        usershows = self.usershow_repo.get_by_show_id(show_id)
        show_animal_count = len(self.show_service.get_by_id_detailed().animals)
>>>>>>> 1181f99 (add show service tests)
||||||| parent of 0206eae (add score tests files)
        usershows = self.usershow_repo.get_by_show_id(show_id)
        show_animal_count = len(self.show_service.get_by_id_detailed().animals)
=======
        usershows = self.usershow_service.get_by_show_id(show_id)
        show_animal_count = len(self.show_service.get_by_id_detailed(show_id).animals)
>>>>>>> 0206eae (add score tests files)
        for us in usershows:
            if self.get_count_by_usershow_id(us.id) != show_animal_count:
                return False
        return True

    def get_users_scored_count(self, show_id: ID) -> NonNegativeInt:
<<<<<<< HEAD
<<<<<<< HEAD
        usershows = self.usershow_service.get_by_show_id(show_id)
        show_animal_count = len(self.show_service.get_by_id_detailed(show_id).animals)
||||||| parent of 1181f99 (add show service tests)
        usershows = self.usershow_repo.get_by_show_id(show_id)
        show_animal_count = len(self.show_service.get_by_id_detailed_animals().animals)
=======
        usershows = self.usershow_repo.get_by_show_id(show_id)
        show_animal_count = len(self.show_service.get_by_id_detailed().animals)
>>>>>>> 1181f99 (add show service tests)
||||||| parent of 0206eae (add score tests files)
        usershows = self.usershow_repo.get_by_show_id(show_id)
        show_animal_count = len(self.show_service.get_by_id_detailed().animals)
=======
        usershows = self.usershow_service.get_by_show_id(show_id)
        show_animal_count = len(self.show_service.get_by_id_detailed(show_id).animals)
>>>>>>> 0206eae (add score tests files)
        count = 0
        for us in usershows:
            if self.get_count_by_usershow_id(us.id) == show_animal_count:
                count += 1
        return count

    def create(self, score_create: ScoreSchemaCreate) -> ScoreSchema:
        new_score = ScoreSchema.from_create(score_create)
        new_score = self.score_repo.create(new_score)

        cur_show_id = self.usershow_service.get_by_id(new_score.usershow_id.value).show_id
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
