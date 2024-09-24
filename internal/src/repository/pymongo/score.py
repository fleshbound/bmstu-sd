import inspect
import json
from typing import List, Optional

from pydantic import NonNegativeInt, BaseModel
from pymongo import MongoClient

from core.show.repository.score import IScoreRepository
from core.show.schema.score import ScoreSchema
import core.utils.types as types
from repository.pymongo.base import PymongoBaseRepository
from repository.pymongo.model.score import ScoreODM
from repository.utils.types import object_id_from_int, int_from_object_id
from utils.exceptions import NotFoundRepoError


class PymongoScoreRepository(IScoreRepository, PymongoBaseRepository):
    client: MongoClient
    collection: str = "score"

    def __init__(self, client: MongoClient):
        self.client = client
        super().__init__(client)

    def get_by_usershow_id(self, usershow_id: NonNegativeInt) -> List[ScoreSchema]:
        res = list(self.database[self.collection].find({'usershowId': usershow_id}))
        return [ScoreODM(**r).to_schema() for r in res]

    def get_by_animalshow_id(self, animalshow_id: NonNegativeInt) -> List[ScoreSchema]:
        res = list(self.database[self.collection].find({'animalshowId': animalshow_id}))
        return [ScoreODM(**r).to_schema() for r in res]

    def get_all(self, skip: int = 0, limit: Optional[int] = None) -> List[ScoreSchema]:
        res = list(self.database[self.collection].find().skip(skip).limit(limit))
        return [ScoreODM(**r).to_schema() for r in res]

    def get_by_id(self, id: NonNegativeInt) -> ScoreSchema:
        res = self.database[self.collection].find_one({'_id': object_id_from_int(id)})
        return ScoreODM(**res).to_schema()

    def create(self, other: ScoreSchema) -> ScoreSchema:
        other_dict = self.get_dict(other, exclude=['id'])
        model_in_json = json.dumps(other_dict)
        new_score = self.database[self.collection].insert_one(document=model_in_json)
        created = self.database[self.collection].full_one({'_id': int_from_object_id(new_score.inserted_id)})
        return ScoreODM(**created).to_schema()

    @staticmethod
    def get_dict(other: BaseModel, exclude: List[str] | None = None) -> dict:
        dct = dict()
        for field in other.model_fields.keys():
            field_value = getattr(other, field)
            if exclude is None or field not in exclude:
                if type(field_value).__name__ in tuple(x[0] for x in inspect.getmembers(types, inspect.isclass)):
                    # if getattr(field_value, '__module__', None) == types.__name__:
                    #     f = fields(field_value)[0]
                    val = getattr(field_value, 'value')
                    dct[field] = val
                else:
                    dct[field] = field_value
        return dct

    def update(self, other: ScoreSchema) -> ScoreSchema:
        pass

    def delete(self, id: NonNegativeInt) -> None:
        try:
            self.database[self.collection].find_one({'_id': object_id_from_int(id)})
        except Exception:
            raise NotFoundRepoError
        self.database[self.collection].delete_one({"_id": object_id_from_int(id)})
