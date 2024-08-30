from abc import ABC, abstractmethod
from typing import List, Tuple

from pydantic import NonNegativeInt

<<<<<<< HEAD
from internal.src.core.show.schema.score import TotalScoreInfo, ScoreSchema, ScoreSchemaCreate, AnimalShowRankingInfo
from internal.src.core.utils.types import ID
||||||| parent of 34b5142 (fix imports)
from core.show.schema.score import TotalScoreInfo, ScoreSchema, ScoreSchemaCreate, AniShowRankingInfo
from core.utils.types import ID
=======
from internal.src.core.show.schema.score import TotalScoreInfo, ScoreSchema, ScoreSchemaCreate, AniShowRankingInfo
from internal.src.core.utils.types import ID
>>>>>>> 34b5142 (fix imports)


class IScoreService(ABC):
    @abstractmethod
    def get_total_by_animalshow_id(self, animalshow_id: ID) -> TotalScoreInfo:
        raise NotImplementedError

    @abstractmethod
    def get_show_ranking_info(self, show_id: ID) -> Tuple[NonNegativeInt, List[AnimalShowRankingInfo]]:
        raise NotImplementedError

    @abstractmethod
    def get_total_by_usershow_id(self, usershow_id: ID) -> TotalScoreInfo:
        raise NotImplementedError

    @abstractmethod
    def all_users_scored(self, show_id: ID) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_users_scored_count(self, show_id: ID) -> NonNegativeInt:
        raise NotImplementedError

    @abstractmethod
    def create(self, score_create: ScoreSchemaCreate) -> ScoreSchema:
        raise NotImplementedError

    @abstractmethod
    def archive(self, id: ID) -> ScoreSchema:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: ID) -> ScoreSchema:
        raise NotImplementedError
