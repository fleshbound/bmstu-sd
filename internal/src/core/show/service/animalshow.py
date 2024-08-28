from abc import ABC, abstractmethod
from typing import List

<<<<<<< HEAD
from internal.src.core.show.schema.animalshow import AnimalShowSchemaCreate, AnimalShowSchema
from internal.src.core.utils.types import ID
||||||| parent of fb32d3b (tests arent working watahel)
from core.show.schema.animalshow import AnimalShowSchemaCreate, AnimalShowSchema
from core.utils.types import ID
=======
from core.show.schema.animalshow import AnimalShowSchemaCreate, AnimalShowSchema, AnimalShowSchemaDeleted
from core.utils.types import ID
>>>>>>> fb32d3b (tests arent working watahel)


class IAnimalShowService(ABC):
    @abstractmethod
    def create(self, animalshow_create: AnimalShowSchemaCreate) -> AnimalShowSchema:
        raise NotImplementedError

    @abstractmethod
    def archive(self, animalshow_id: ID) -> AnimalShowSchema:
        raise NotImplementedError

    @abstractmethod
    def delete(self, animalshow_id: ID) -> AnimalShowSchemaDeleted:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: ID) -> AnimalShowSchema:
        raise NotImplementedError

    @abstractmethod
    def get_by_animal_id(self, animal_id: ID) -> List[AnimalShowSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_show_id(self, show_id: ID) -> List[AnimalShowSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_animal_show_id(self, animal_id: ID, show_id: ID) -> AnimalShowSchema:
        raise NotImplementedError
