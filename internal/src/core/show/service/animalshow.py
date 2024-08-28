from abc import ABC, abstractmethod
from typing import List

from internal.src.core.show.schema.animalshow import AnimalShowSchemaCreate, AnimalShowSchema, AnimalShowSchemaDeleted
from internal.src.core.utils.types import ID


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
