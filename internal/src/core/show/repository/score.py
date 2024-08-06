from abc import abstractmethod, ABC
from typing import List

from pydantic import NonNegativeInt

from core.show.schema.score import ScoreSchema


class IScoreRepository(ABC):
    @abstractmethod
    def get_by_animalshow_id(self, animalshow_id: NonNegativeInt) -> List[ScoreSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_usershow_id(self, usershow_id: NonNegativeInt) -> List[ScoreSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ScoreSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: NonNegativeInt) -> ScoreSchema:
        raise NotImplementedError

    @abstractmethod
    def create(self, object: ScoreSchema) -> ScoreSchema:
        raise NotImplementedError

    @abstractmethod
    def update(self, object: ScoreSchema) -> ScoreSchema:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: NonNegativeInt) -> None:
        raise NotImplementedError
