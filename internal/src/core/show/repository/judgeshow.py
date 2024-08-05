from abc import abstractmethod, ABC
from typing import List

from pydantic import NonNegativeInt

from core.show.schema.judgeshow import JudgeShowSchema, JudgeShowSchemaCreate, JudgeShowSchemaUpdate


class IJudgeShowRepository(ABC):
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[JudgeShowSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: NonNegativeInt) -> JudgeShowSchema:
        raise NotImplementedError

    @abstractmethod
    def create(self, object: JudgeShowSchemaCreate) -> JudgeShowSchema:
        raise NotImplementedError

    @abstractmethod
    def update(self, object: JudgeShowSchemaUpdate) -> JudgeShowSchema:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: NonNegativeInt) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_user_id(self, user_id: NonNegativeInt) -> List[JudgeShowSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_show_id(self, animal_id: NonNegativeInt) -> List[JudgeShowSchema]:
        raise NotImplementedError
