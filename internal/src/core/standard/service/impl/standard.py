from typing import List

from pydantic import NonNegativeInt, PositiveInt

from internal.src.core.animal.schema.animal import AnimalSchema
from internal.src.core.show.service.show import IShowService
from internal.src.core.standard.repository.standard import IStandardRepository
from internal.src.core.standard.schema.standard import StandardSchema, StandardSchemaCreate, \
    StandardSchemaDeleteResponse
from internal.src.core.standard.service.standard import IStandardService
from internal.src.core.utils.exceptions import CheckAnimalStandardError, CheckAnimalBreedError, \
    NotFoundRepoError, StandardInUseError
from internal.src.core.utils.types import ID, Weight


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

    def is_standard_used(self, id: ID) -> bool:
        try:
            self.show_service.get_by_standard_id(id)
        except NotFoundRepoError:
            return False
        return True

    def delete(self, id: ID) -> StandardSchemaDeleteResponse:
        if self.is_standard_used(id):
            raise StandardInUseError(standard_id=id)

        self.standard_repo.delete(id)
        return StandardSchemaDeleteResponse(id=id)

    @staticmethod
    def check_animal_weight(animal: AnimalSchema, standard: StandardSchema):
        lo_weight = standard.weight * (100 - standard.weight_delta_percent) / Weight(100)
        hi_weight = standard.weight * (100 + standard.weight_delta_percent) / Weight(100)
        if animal.weight < lo_weight or animal.weight > hi_weight:
            raise CheckAnimalStandardError(animal_id=animal.id, standard_id=standard.id, property_name='weight')

    @staticmethod
    def check_animal_length(animal: AnimalSchema, standard: StandardSchema):
        lo_length = standard.length * (100 - standard.length_delta_percent) / Weight(100)
        hi_length = standard.length * (100 + standard.length_delta_percent) / Weight(100)
        if animal.length < lo_length or animal.length > hi_length:
            raise CheckAnimalStandardError(animal_id=animal.id, standard_id=standard.id, property_name='length')

    @staticmethod
    def check_animal_height(animal: AnimalSchema, standard: StandardSchema):
        lo_height = standard.height * (100 - standard.height_delta_percent) / Weight(100)
        hi_height = standard.height * (100 + standard.height_delta_percent) / Weight(100)
        if animal.height < lo_height or animal.height > hi_height:
            raise CheckAnimalStandardError(animal_id=animal.id, standard_id=standard.id, property_name='height')

    def check_animal_by_standard(self, standard_id: ID, animal: AnimalSchema):
        cur_standard = self.standard_repo.get_by_id(standard_id)

        if cur_standard.breed_id != animal.breed_id:
            raise CheckAnimalBreedError(animal_id=animal.id, standard_id=standard_id)

        self.check_animal_weight(animal, cur_standard)
        self.check_animal_height(animal, cur_standard)
        self.check_animal_length(animal, cur_standard)

        if animal.has_defects != cur_standard.has_defects:
            raise CheckAnimalStandardError(animal_id=animal.id, standard_id=standard_id, property_name='has_defects')

        if animal.is_multicolor != cur_standard.is_multicolor:
            raise CheckAnimalStandardError(animal_id=animal.id, standard_id=standard_id, property_name='is_multicolor')

        return True
