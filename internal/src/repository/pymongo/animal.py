import inspect
import json
from typing import List, Optional

from pydantic import NonNegativeInt, BaseModel
from pymongo import MongoClient

from core.animal.repository.animal import IAnimalRepository
from core.animal.schema.animal import AnimalSchema
import core.utils.types as types
from repository.pymongo.base import PymongoBaseRepository
from repository.pymongo.model.animal import AnimalODM
from repository.utils.types import object_id_from_int, int_from_object_id
from utils.exceptions import NotFoundRepoError


class PymongoAnimalRepository(IAnimalRepository, PymongoBaseRepository):
    client: MongoClient
    collection: str = "animal"

    def __init__(self, client: MongoClient):
        self.client = client
        super().__init__(client)

    def get_by_user_id(self, user_id: NonNegativeInt) -> List[AnimalSchema]:
        res = list(self.database[self.collection].find({'userId': user_id}))
        return [AnimalODM(**r).to_schema() for r in res]

    def get_all(self, skip: int = 0, limit: Optional[int] = None) -> List[AnimalSchema]:
        res = list(self.database[self.collection].find().skip(skip).limit(limit))
        return [AnimalODM(**r).to_schema() for r in res]

    def get_by_id(self, id: NonNegativeInt) -> AnimalSchema:
        res = self.database[self.collection].find_one({'_id': object_id_from_int(id)})
        return AnimalODM(**res).to_schema()

    def create(self, other: AnimalSchema) -> AnimalSchema:
        other_dict = self.get_dict(other, exclude=['id'])
        model_in_json = json.dumps(other_dict)
        new_animal = self.database[self.collection].insert_one(document=model_in_json)
        created = self.database[self.collection].full_one({'_id': int_from_object_id(new_animal.inserted_id)})
        return AnimalODM(**created).to_schema()

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

    def update(self, other: AnimalSchema) -> AnimalSchema:
        pass

    def delete(self, id: NonNegativeInt) -> None:
        try:
            self.database[self.collection].find_one({'_id': object_id_from_int(id)})
        except Exception:
            raise NotFoundRepoError
        self.database[self.collection].delete_one({"_id": object_id_from_int(id)})
