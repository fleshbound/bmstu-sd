from typing import List

from pydantic import NonNegativeInt, PositiveInt

from internal.src.core.animal.schema.animal import AnimalSchema, AnimalSchemaDelete, AnimalSchemaCreate, \
    AnimalSchemaUpdate
from internal.src.core.animal.service.animal import IAnimalService
from internal.src.core.utils.exceptions import NotFoundRepoError
from internal.src.core.utils.types import ID


class MockedAnimalService(IAnimalService):
    _animals: List[AnimalSchema]

    def __init__(self, animals: List[AnimalSchema]):
        self._animals = animals

    def delete(self,
               animal_id: ID) -> AnimalSchemaDelete:
        return AnimalSchemaDelete(id=animal_id)

    def create(self,
               create_animal: AnimalSchemaCreate) -> AnimalSchema:
        self._animals.append(AnimalSchema.from_create(create_animal))
        if len(self._animals) > 0:
            self._animals[-1].id = ID(len(self._animals) - 1)
        else:
            self._animals[-1].id = ID(0)
        return self._animals[-1]

    def update(self,
               update_animal: AnimalSchemaUpdate) -> AnimalSchema:
        for animal in self._animals:
            if animal.id == update_animal.id:
                animal = animal.from_update(update_animal)
                return animal
        raise NotFoundRepoError(detail='')

    def get_all(self,
                skip: NonNegativeInt = 0,
                limit: PositiveInt = 100) -> List[AnimalSchema]:
        return self._animals

    def get_by_user_id(self,
                       user_id: ID) -> List[AnimalSchema]:
        res = []
        for animal in self._animals:
            if animal.user_id == user_id:
                res.append(animal)
        if len(res) == 0:
            raise NotFoundRepoError(detail='')
        return res

    def get_by_id(self, animal_id: ID) -> AnimalSchema:
        for animal in self._animals:
            if animal.user_id == animal_id:
                return animal
    