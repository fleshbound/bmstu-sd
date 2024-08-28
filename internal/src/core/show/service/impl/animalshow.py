from typing import List

<<<<<<< HEAD
<<<<<<< HEAD
from internal.src.core.show.repository.animalshow import IAnimalShowRepository
from internal.src.core.show.schema.animalshow import AnimalShowSchemaCreate, AnimalShowSchema, AnimalShowSchemaDeleted
from internal.src.core.show.service.animalshow import IAnimalShowService
from internal.src.core.utils.types import ID
||||||| parent of fb32d3b (tests arent working watahel)
from core.show.repository.animalshow import IAnimalShowRepository
from core.show.schema.animalshow import AnimalShowSchemaCreate, AnimalShowSchema, AnimalShowSchemaDeleted
from core.show.service.animalshow import IAnimalShowService
from core.utils.types import ID
=======
from core.show.repository.animalshow import IAnimalShowRepository
from core.show.schema.animalshow import AnimalShowSchemaCreate, AnimalShowSchema, AnimalShowSchemaDeleted
from core.show.service.animalshow import IAnimalShowService
from core.utils.exceptions import AnimalShowServiceError
from core.utils.types import ID
>>>>>>> fb32d3b (tests arent working watahel)
||||||| parent of d8bdfb9 (add animal tests (init))
from core.show.repository.animalshow import IAnimalShowRepository
from core.show.schema.animalshow import AnimalShowSchemaCreate, AnimalShowSchema, AnimalShowSchemaDeleted
from core.show.service.animalshow import IAnimalShowService
from core.utils.exceptions import AnimalShowServiceError
from core.utils.types import ID
=======
from internal.src.core.show.repository.animalshow import IAnimalShowRepository
from internal.src.core.show.schema.animalshow import AnimalShowSchemaCreate, AnimalShowSchema, AnimalShowSchemaDeleted
from internal.src.core.show.service.animalshow import IAnimalShowService
from internal.src.core.utils.exceptions import AnimalShowServiceError
from internal.src.core.utils.types import ID
>>>>>>> d8bdfb9 (add animal tests (init))


class AnimalShowService(IAnimalShowService):
    animalshow_repo: IAnimalShowRepository

    def __init__(self, animalshow_repo: IAnimalShowRepository):
        self.animalshow_repo = animalshow_repo

    def create(self, animalshow_create: AnimalShowSchemaCreate) -> AnimalShowSchema:
        new_animalshow = AnimalShowSchema.from_create(animalshow_create)
        return self.animalshow_repo.create(new_animalshow)

    def archive(self, animalshow_id: ID) -> AnimalShowSchema:
        cur_animalshow = self.animalshow_repo.get_by_id(animalshow_id.value)
        cur_animalshow.is_archived = True
        return self.animalshow_repo.update(cur_animalshow)

    def delete(self, animalshow_id: ID) -> AnimalShowSchemaDeleted:
        self.animalshow_repo.delete(animalshow_id)
        return AnimalShowSchemaDeleted(id=animalshow_id)
    
    def get_by_id(self, id: ID) -> AnimalShowSchema:
        return self.animalshow_repo.get_by_id(id.value)
    
    def get_by_animal_id(self, animal_id: ID) -> List[AnimalShowSchema]:
        return self.animalshow_repo.get_by_animal_id(animal_id.value)

    def get_by_show_id(self, show_id: ID) -> List[AnimalShowSchema]:
        return self.animalshow_repo.get_by_show_id(show_id.value)

    def get_by_animal_show_id(self, animal_id: ID, show_id: ID) -> AnimalShowSchema:
        res = self.animalshow_repo.get_by_animal_show_id(animal_id.value, show_id.value)
        if len(res) > 0:
            raise AnimalShowServiceError(detail='More than one animalshow record')
        return res[0]
