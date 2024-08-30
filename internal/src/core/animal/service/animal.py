from abc import ABC, abstractmethod
from typing import List

from pydantic import NonNegativeInt, PositiveInt

<<<<<<< HEAD
<<<<<<< HEAD
from internal.src.core.animal.schema.animal import AnimalSchema, AnimalSchemaUpdate, AnimalSchemaCreate, AnimalSchemaDelete
from internal.src.core.utils.types import ID
||||||| parent of fb32d3b (tests arent working watahel)
from core.animal.schema.animal import AnimalSchema, AnimalSchemaUpdate, AnimalSchemaCreate, AnimalSchemaDelete
from core.utils.types import ID
=======
||||||| parent of 9dbb4c9 (fix imports)
=======
<<<<<<< HEAD
>>>>>>> 9dbb4c9 (fix imports)
from internal.src.core.animal.schema.animal import AnimalSchema, AnimalSchemaUpdate, AnimalSchemaCreate, \
    AnimalSchemaDelete
from internal.src.core.utils.types import ID
<<<<<<< HEAD
>>>>>>> fb32d3b (tests arent working watahel)
||||||| parent of 9dbb4c9 (fix imports)
=======
||||||| parent of 34b5142 (fix imports)
from core.animal.schema.animal import AnimalSchema, AnimalSchemaUpdate, AnimalSchemaCreate, AnimalSchemaDelete
from core.utils.types import ID
=======
from internal.src.core.animal.schema.animal import AnimalSchema, AnimalSchemaUpdate, AnimalSchemaCreate, AnimalSchemaDelete
from internal.src.core.utils.types import ID
>>>>>>> 34b5142 (fix imports)
>>>>>>> 9dbb4c9 (fix imports)


class IAnimalService(ABC):
    @abstractmethod
    def delete(self,
                animal_id: ID) -> AnimalSchemaDelete:
        raise NotImplementedError

    @abstractmethod
    def create(self,
               create_animal: AnimalSchemaCreate) -> AnimalSchema:
        raise NotImplementedError

    @abstractmethod
    def update(self,
               update_animal: AnimalSchemaUpdate) -> AnimalSchema:
        raise NotImplementedError

    @abstractmethod
    def get_all(self,
                skip: NonNegativeInt = 0,
                limit: PositiveInt = 100) -> List[AnimalSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_user_id(self,
                       user_id: ID) -> List[AnimalSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, animal_id: ID) -> AnimalSchema:
        raise NotImplementedError
