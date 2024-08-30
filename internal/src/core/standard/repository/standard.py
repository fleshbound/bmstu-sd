from abc import abstractmethod, ABC
from typing import List

from pydantic import NonNegativeInt

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from internal.src.core.standard.schema.standard import StandardSchema, StandardSchemaCreate
||||||| parent of fb32d3b (tests arent working watahel)
from core.standard.schema.standard import StandardSchema, StandardSchemaCreate
=======
from core.standard.schema.standard import StandardSchema
>>>>>>> fb32d3b (tests arent working watahel)
||||||| parent of d8bdfb9 (add animal tests (init))
from core.standard.schema.standard import StandardSchema
=======
||||||| parent of 9dbb4c9 (fix imports)
=======
<<<<<<< HEAD
>>>>>>> 9dbb4c9 (fix imports)
from internal.src.core.standard.schema.standard import StandardSchema
<<<<<<< HEAD
>>>>>>> d8bdfb9 (add animal tests (init))
||||||| parent of 9dbb4c9 (fix imports)
=======
||||||| parent of 34b5142 (fix imports)
from core.standard.schema.standard import StandardSchema, StandardSchemaCreate
=======
from internal.src.core.standard.schema.standard import StandardSchema, StandardSchemaCreate
>>>>>>> 34b5142 (fix imports)
>>>>>>> 9dbb4c9 (fix imports)


class IStandardRepository(ABC):
    @abstractmethod
    def get_by_breed_id(self, breed_id: NonNegativeInt) -> List[StandardSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[StandardSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: NonNegativeInt) -> StandardSchema:
        raise NotImplementedError

    @abstractmethod
    def create(self, object: StandardSchema) -> StandardSchema:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: NonNegativeInt) -> None:
        raise NotImplementedError

    # @abstractmethod
    # def update(self, object: StandardSchema) -> StandardSchema:
    #     raise NotImplementedError
