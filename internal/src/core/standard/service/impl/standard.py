from typing import List

from fastapi import HTTPException
from pydantic import NonNegativeInt, PositiveInt

<<<<<<< HEAD
from internal.src.core.animal.schema.animal import AnimalSchema
from internal.src.core.show.service.show import IShowService
from internal.src.core.standard.repository.standard import IStandardRepository
from internal.src.core.standard.schema.standard import StandardSchema, StandardSchemaCreate, StandardSchemaDeleteResponse
from internal.src.core.standard.service.standard import IStandardService
from internal.src.core.utils.exceptions import StandardServiceError
from internal.src.core.utils.types import ID, Weight
||||||| parent of 34b5142 (fix imports)
from core.animal.schema.animal import AnimalSchema
from core.show.service.show import IShowService
from core.standard.repository.standard import IStandardRepository
from core.standard.schema.standard import StandardSchema, StandardSchemaCreate, StandardSchemaDeleteResponse
from core.standard.service.standard import IStandardService
from core.utils.exceptions import StandardServiceError
from core.utils.types import ID
=======
from internal.src.core.animal.schema.animal import AnimalSchema
from internal.src.core.show.service.show import IShowService
from internal.src.core.standard.repository.standard import IStandardRepository
from internal.src.core.standard.schema.standard import StandardSchema, StandardSchemaCreate, StandardSchemaDeleteResponse
from internal.src.core.standard.service.standard import IStandardService
from internal.src.core.utils.exceptions import StandardServiceError
from internal.src.core.utils.types import ID
>>>>>>> 34b5142 (fix imports)


class StandardService(IStandardService):
    standard_repo: IStandardRepository
    show_service: IShowService

    def __init__(self, standard_repo: IStandardRepository, show_service: IShowService):
        self.standard_repo = standard_repo
        self.show_service = show_service

    def get_by_breed_id(self, breed_id: ID) -> List[StandardSchema]:
        return self.standard_repo.get_by_breed_id(breed_id.value)

    def get_all(self, skip: NonNegativeInt = 0, limit: PositiveInt = 100) -> List[StandardSchema]:
        return self.standard_repo.get_all(skip, limit)

    def get_by_id(self, id: ID) -> StandardSchema:
        return self.get_by_id(id.value)

    def create(self, standard_create: StandardSchemaCreate) -> StandardSchema:
        new_standard = StandardSchema.from_create(standard_create)
        return self.standard_repo.create(new_standard)

    def delete(self, id: ID) -> StandardSchemaDeleteResponse:
        try:
            self.show_service.get_by_standard_id(id)
        except HTTPException:
            self.standard_repo.delete(id)
            return StandardSchemaDeleteResponse(id=id)
        raise StandardServiceError(detail=f'standard\'s in use: standard_id={id}')

    def check_animal_by_standard(self, standard_id: ID, animal: AnimalSchema) -> bool:
        cur_standard = self.standard_repo.get_by_id(standard_id)

        if cur_standard.breed_id != animal.breed_id:
            raise StandardServiceError(detail=f'breed_id must be equal: standard_id={standard_id},'
                                              f' animal_id={animal.id.value}')

        lo_weight = cur_standard.weight * (100 - cur_standard.weight_delta_percent) / Weight(100)
        hi_weight = cur_standard.weight * (100 + cur_standard.weight_delta_percent) / Weight(100)
        if animal.weight < lo_weight or animal.weight > hi_weight:
            return False

        lo_height = cur_standard.height * (100 - cur_standard.height_delta_percent) / Weight(100)
        hi_height = cur_standard.height * (100 + cur_standard.height_delta_percent) / Weight(100)
        if animal.height < lo_height or animal.height > hi_height:
            return False

        lo_length = cur_standard.length * (100 - cur_standard.length_delta_percent) / Weight(100)
        hi_length = cur_standard.length * (100 + cur_standard.length_delta_percent) / Weight(100)
        if animal.length < lo_length or animal.length > hi_length:
            return False

        if animal.has_defects != cur_standard.has_defects:
            return False

        if animal.is_multicolor != cur_standard.is_multicolor:
            return False

        return True
