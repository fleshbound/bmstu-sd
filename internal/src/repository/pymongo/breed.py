import inspect
import json
from typing import List, Optional

from pydantic import NonNegativeInt, BaseModel
from pymongo import MongoClient

from core.breed.repository.breed import IBreedRepository
from core.breed.schema.breed import BreedSchema
import core.utils.types as types
from repository.pymongo.base import PymongoBaseRepository
from repository.pymongo.model.breed import BreedODM
from repository.utils.types import object_id_from_int, int_from_object_id
from utils.exceptions import NotFoundRepoError


class PymongoBreedRepository(IBreedRepository, PymongoBaseRepository):
    client: MongoClient
    collection: str = "breed"

    def __init__(self, client: MongoClient):
        self.client = client
        super().__init__(client)

    def get_by_species_id(self, species_id: NonNegativeInt) -> List[BreedSchema]:
        res = list(self.database[self.collection].find({'speciesId': species_id}))
        return [BreedODM(**r).to_schema() for r in res]

    def get_all(self, skip: int = 0, limit: Optional[int] = None) -> List[BreedSchema]:
        res = list(self.database[self.collection].find().skip(skip).limit(limit))
        return [BreedODM(**r).to_schema() for r in res]

    def get_by_id(self, id: NonNegativeInt) -> BreedSchema:
        res = self.database[self.collection].find_one({'_id': object_id_from_int(id)})
        return BreedODM(**res).to_schema()

    def create(self, other: BreedSchema) -> BreedSchema:
        other_dict = self.get_dict(other, exclude=['id'])
        model_in_json = json.dumps(other_dict)
        new_breed = self.database[self.collection].insert_one(document=model_in_json)
        created = self.database[self.collection].full_one({'_id': int_from_object_id(new_breed.inserted_id)})
        return BreedODM(**created).to_schema()

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

    def update(self, other: BreedSchema) -> BreedSchema:
        pass

    def delete(self, id: NonNegativeInt) -> None:
        try:
            self.database[self.collection].find_one({'_id': object_id_from_int(id)})
        except Exception:
            raise NotFoundRepoError
        self.database[self.collection].delete_one({"_id": object_id_from_int(id)})
