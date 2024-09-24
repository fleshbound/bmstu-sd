import inspect
import json
from typing import List, Optional

from pydantic import NonNegativeInt, BaseModel
from pymongo import MongoClient

from core.standard.repository.standard import IStandardRepository
from core.standard.schema.standard import StandardSchema
import core.utils.types as types
from repository.pymongo.base import PymongoBaseRepository
from repository.pymongo.model.standard import StandardODM
from repository.utils.types import object_id_from_int, int_from_object_id
from utils.exceptions import NotFoundRepoError


class PymongoStandardRepository(IStandardRepository, PymongoBaseRepository):
    client: MongoClient
    collection: str = "standard"

    def __init__(self, client: MongoClient):
        self.client = client
        super().__init__(client)

    def get_by_breed_id(self, breed_id: NonNegativeInt) -> List[StandardSchema]:
        res = list(self.database[self.collection].find({'breedId': breed_id}))
        return [StandardODM(**r).to_schema() for r in res]

    def get_all(self, skip: int = 0, limit: Optional[int] = None) -> List[StandardSchema]:
        res = list(self.database[self.collection].find().skip(skip).limit(limit))
        return [StandardODM(**r).to_schema() for r in res]

    def get_by_id(self, id: NonNegativeInt) -> StandardSchema:
        res = self.database[self.collection].find_one({'_id': object_id_from_int(id)})
        return StandardODM(**res).to_schema()

    def create(self, other: StandardSchema) -> StandardSchema:
        other_dict = self.get_dict(other, exclude=['id'])
        model_in_json = json.dumps(other_dict)
        new_standard = self.database[self.collection].insert_one(document=model_in_json)
        created = self.database[self.collection].full_one({'_id': int_from_object_id(new_standard.inserted_id)})
        return StandardODM(**created).to_schema()

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

    def update(self, other: StandardSchema) -> StandardSchema:
        pass

    def delete(self, id: NonNegativeInt) -> None:
        try:
            self.database[self.collection].find_one({'_id': object_id_from_int(id)})
        except Exception:
            raise NotFoundRepoError
        self.database[self.collection].delete_one({"_id": object_id_from_int(id)})
