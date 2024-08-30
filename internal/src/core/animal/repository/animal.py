from abc import abstractmethod, ABC
from typing import List

from pydantic import NonNegativeInt
<<<<<<< HEAD

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from internal.src.core.animal.schema.animal import AnimalSchema, AnimalSchemaCreate, AnimalSchemaUpdate
||||||| parent of fb32d3b (tests arent working watahel)
from core.animal.schema.animal import AnimalSchema, AnimalSchemaCreate, AnimalSchemaUpdate
=======
from core.animal.schema.animal import AnimalSchema
>>>>>>> fb32d3b (tests arent working watahel)
||||||| parent of d8bdfb9 (add animal tests (init))
from core.animal.schema.animal import AnimalSchema
=======
||||||| parent of 9dbb4c9 (fix imports)
=======
<<<<<<< HEAD
>>>>>>> 9dbb4c9 (fix imports)
||||||| parent of a4e4ef4 (fix conflicts)

<<<<<<< HEAD
=======
>>>>>>> a4e4ef4 (fix conflicts)
from internal.src.core.animal.schema.animal import AnimalSchema
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> d8bdfb9 (add animal tests (init))
||||||| parent of 9dbb4c9 (fix imports)
=======
||||||| parent of 34b5142 (fix imports)
from core.animal.schema.animal import AnimalSchema, AnimalSchemaCreate, AnimalSchemaUpdate
=======
from internal.src.core.animal.schema.animal import AnimalSchema, AnimalSchemaCreate, AnimalSchemaUpdate
>>>>>>> 34b5142 (fix imports)
>>>>>>> 9dbb4c9 (fix imports)
||||||| parent of a4e4ef4 (fix conflicts)
||||||| parent of 34b5142 (fix imports)
from core.animal.schema.animal import AnimalSchema, AnimalSchemaCreate, AnimalSchemaUpdate
=======
from internal.src.core.animal.schema.animal import AnimalSchema, AnimalSchemaCreate, AnimalSchemaUpdate
>>>>>>> 34b5142 (fix imports)
=======
>>>>>>> a4e4ef4 (fix conflicts)


class IAnimalRepository(ABC):
    @abstractmethod
    def get_by_user_id(self, user_id: NonNegativeInt) -> List[AnimalSchema]:
        raise NotImplementedError
               
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[AnimalSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: NonNegativeInt) -> AnimalSchema:
        raise NotImplementedError

    @abstractmethod
    def create(self, other: AnimalSchema) -> AnimalSchema:
        raise NotImplementedError

    @abstractmethod
    def update(self, other: AnimalSchema) -> AnimalSchema:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: NonNegativeInt) -> None:
        raise NotImplementedError
