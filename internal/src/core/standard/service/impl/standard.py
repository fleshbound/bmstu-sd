from typing import List

from pydantic import NonNegativeInt, PositiveInt

from core.animal.schema.animal import AnimalSchema
from core.show.service.show import IShowService
from core.standard.repository.standard import IStandardRepository
from core.standard.schema.standard import StandardSchema, StandardSchemaCreate, StandardSchemaDeleteResponse
from core.standard.service.standard import IStandardService
from utils.exceptions import StandardServiceError
from utils.types import ID


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
        if len(self.show_service.get_by_standard_id(id)) > 0:
            raise StandardServiceError(detail=f'standard is in use: standard_id={id}')
        self.standard_repo.delete(id)
        return StandardSchemaDeleteResponse(id=id)

    def check_animal_by_standard(self, standard_id: ID, animal: AnimalSchema) -> bool:
        cur_standard = self.standard_repo.get_by_id(standard_id)

        if cur_standard.breed_id != animal.breed_id:
            raise StandardServiceError(detail=f'breed_id must be equal: standard_id={standard_id},'
                                              f' animal_id={animal.id.value}')

        lo_weight = cur_standard.weight * (1 - cur_standard.weight_delta_percent)
        hi_weight = cur_standard.weight * (1 + cur_standard.weight_delta_percent)
        if animal.weight < lo_weight or animal.weight > hi_weight:
            return False

        lo_height = cur_standard.height * (1 - cur_standard.height_delta_percent)
        hi_height = cur_standard.height * (1 + cur_standard.height_delta_percent)
        if animal.height < lo_height or animal.height > hi_height:
            return False

        lo_prolixity_index = cur_standard.prolixity_index * (1 - cur_standard.prolixity_index_delta_percent)
        hi_prolixity_index = cur_standard.prolixity_index * (1 + cur_standard.prolixity_index_delta_percent)
        if animal.prolixity_index < lo_prolixity_index or animal.prolixity_index > hi_prolixity_index:
            return False

        if animal.has_defects != cur_standard.has_defects:
            return False

        if animal.is_multicolor != cur_standard.is_multi_color:
            return False

        return True
