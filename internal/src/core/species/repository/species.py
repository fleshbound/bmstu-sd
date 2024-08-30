from abc import abstractmethod, ABC
from typing import List

from pydantic import NonNegativeInt

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from internal.src.core.species.schema.species import SpeciesSchema, SpeciesSchemaCreate, SpeciesSchemaUpdate
||||||| parent of fb32d3b (tests arent working watahel)
from core.species.schema.species import SpeciesSchema, SpeciesSchemaCreate, SpeciesSchemaUpdate
=======
from core.species.schema.species import SpeciesSchema
>>>>>>> fb32d3b (tests arent working watahel)
||||||| parent of d8bdfb9 (add animal tests (init))
from core.species.schema.species import SpeciesSchema
=======
||||||| parent of 9dbb4c9 (fix imports)
=======
<<<<<<< HEAD
>>>>>>> 9dbb4c9 (fix imports)
from internal.src.core.species.schema.species import SpeciesSchema
<<<<<<< HEAD
>>>>>>> d8bdfb9 (add animal tests (init))
||||||| parent of 9dbb4c9 (fix imports)
=======
||||||| parent of 34b5142 (fix imports)
from core.species.schema.species import SpeciesSchema, SpeciesSchemaCreate, SpeciesSchemaUpdate
=======
from internal.src.core.species.schema.species import SpeciesSchema, SpeciesSchemaCreate, SpeciesSchemaUpdate
>>>>>>> 34b5142 (fix imports)
>>>>>>> 9dbb4c9 (fix imports)


class ISpeciesRepository(ABC):
    @abstractmethod
    def get_by_group_id(self, group_id: NonNegativeInt) -> List[SpeciesSchema]:
        raise NotImplementedError
               
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[SpeciesSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: NonNegativeInt) -> SpeciesSchema:
        raise NotImplementedError

    @abstractmethod
    def create(self, object: SpeciesSchema) -> SpeciesSchema:
        raise NotImplementedError

    @abstractmethod
    def update(self, object: SpeciesSchema) -> SpeciesSchema:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: NonNegativeInt) -> None:
        raise NotImplementedError
