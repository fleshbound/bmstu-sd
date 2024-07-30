from typing import List

from pydantic import NonNegativeInt, PositiveInt

from core.animal.repository.animal import IAnimalRepository
from core.animal.schema.animal import AnimalSchema, AnimalSchemaCreate, AnimalSchemaUpdate
from core.animal.service.animal import IAnimalService
from utils.types import ID


class AnimalService(IAnimalService):
    animal_repo: IAnimalRepository

    def __init__(self,
                 animal_repo: IAnimalRepository):
        self.animal_repo = animal_repo

    def archive(self,
                animal_id: ID) -> AnimalSchema:
        animal: AnimalSchema = self.animal_repo.get_by_id(animal_id)
        animal.is_archived = True
        return self.animal_repo.update(animal)

    def create(self,
               create_animal: AnimalSchemaCreate) -> AnimalSchema:
        return self.animal_repo.create(create_animal)

    def update(self,
               update_animal: AnimalSchemaUpdate) -> AnimalSchema:
        return self.animal_repo.update(update_animal)

    def get_all(self,
                skip: NonNegativeInt = 0,
                limit: PositiveInt = 100) -> List[AnimalSchema]:
        return self.animal_repo.get_all(skip, limit)

    def get_by_user_id(self,
                       user_id: ID) -> List[AnimalSchema]:
        return self.animal_repo.get_by_user_id(user_id.value)

    def get_by_id(self, animal_id: ID) -> AnimalSchema:
        return self.animal_repo.get_by_id(animal_id.value)