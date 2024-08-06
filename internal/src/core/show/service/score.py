from abc import ABC, abstractmethod
from typing import List

from core.show.schema.score import TotalScoreInfo, ScoreSchema, ScoreSchemaCreate, ScoreSchemaUpdate, ScoreID
from utils.types import ID


class IScoreService(ABC):
    @abstractmethod
    def get_total_by_animalshow_id(self, animalshow_id: ID) -> TotalScoreInfo:
        raise NotImplementedError

    @abstractmethod
    def get_total_by_usershow_id(self, usershow_id: ID) -> TotalScoreInfo:
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
