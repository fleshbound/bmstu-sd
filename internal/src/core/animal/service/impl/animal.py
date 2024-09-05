from typing import List

from pydantic import NonNegativeInt, PositiveInt

from internal.src.core.animal.repository.animal import IAnimalRepository
from internal.src.core.animal.schema.animal import AnimalSchema, AnimalSchemaCreate, AnimalSchemaUpdate, \
    AnimalSchemaDelete
from internal.src.core.animal.service.animal import IAnimalService
from internal.src.core.show.schema.animalshow import AnimalShowSchema
from internal.src.core.show.schema.show import ShowStatus
from internal.src.core.show.service.animalshow import IAnimalShowService
from internal.src.core.show.service.show import IShowService
from internal.src.core.utils.exceptions import NotFoundRepoError, DeleteAnimalStartedShowError
from internal.src.core.utils.types import ID


class AnimalService(IAnimalService):
    animal_repo: IAnimalRepository
    animalshow_service: IAnimalShowService
    show_service: IShowService

    def __init__(self, animal_repo: IAnimalRepository, animalshow_service: IAnimalShowService,
                 show_service: IShowService):
        self.animal_repo = animal_repo
        self.animalshow_service = animalshow_service
        self.show_service = show_service

    def get_animal_registration_records(self, animal_id: ID) -> List[AnimalShowSchema]:
        try:
            records = self.animalshow_service.get_by_animal_id(animal_id)
        except NotFoundRepoError:
            return []
        return records

    def delete(self, animal_id: ID) -> AnimalSchemaDelete:
        if not (animal_registration_records := self.get_animal_registration_records(animal_id)):
            self.animal_repo.delete(animal_id)
            return AnimalSchemaDelete(id=animal_id)

        shows = []
        for record in animal_registration_records:
            cur_show = self.show_service.get_by_id(record.show_id)
            if cur_show.status == ShowStatus.started:
                raise DeleteAnimalStartedShowError(animal_id=animal_id)
            shows.append(cur_show)

        for i, show in enumerate(shows):
            if show.status == ShowStatus.created:
                self.show_service.unregister_animal(animal_id, show.id)
            else:
                self.animalshow_service.archive(animal_registration_records[i].id)

        self.animal_repo.delete(animal_id)
        return AnimalSchemaDelete(id=animal_id)

    def create(self, create_animal: AnimalSchemaCreate) -> AnimalSchema:
        new_animal = AnimalSchema.from_create(create_animal)
        return self.animal_repo.create(new_animal)

    def update(self, update_animal: AnimalSchemaUpdate) -> AnimalSchema:
        cur_animal = self.animal_repo.get_by_id(update_animal.id.value)
        cur_animal = cur_animal.from_update(update_animal)
        return self.animal_repo.update(cur_animal)

    def get_all(self, skip: NonNegativeInt = 0, limit: PositiveInt = 100) -> List[AnimalSchema]:
        return self.animal_repo.get_all(skip, limit)

    def get_by_user_id(self, user_id: ID) -> List[AnimalSchema]:
        return self.animal_repo.get_by_user_id(user_id.value)

    def get_by_id(self, animal_id: ID) -> AnimalSchema:
        return self.animal_repo.get_by_id(animal_id.value)
