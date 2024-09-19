from console.tech.utils.lang.langmodel import LanguageModel
from core.animal.service.animal import IAnimalService
from core.show.service.show import IShowService

from console.tech.dto.animal import AnimalDTO
from console.tech.utils.exceptions import InputException
from core.utils.exceptions import DeleteAnimalStartedShowError, NotFoundRepoError
from core.utils.types import ID


class AnimalHandler:
    animal_service: IAnimalService
    show_service: IShowService
    lm: LanguageModel

    def __init__(self,
                 animal_service: IAnimalService,
                 show_service: IShowService):
        self.animal_service = animal_service
        self.show_service = show_service

    def get_animals_by_user_id(self, user_id: int) -> None:
        try:
            res = self.animal_service.get_by_user_id(ID(user_id))
        except NotFoundRepoError:
            print(self.lm.get_empty_result)
            return
        for animal in res:
            AnimalDTO.from_schema(animal).print()

    def delete_animal(self) -> None:
        try:
            dto: AnimalDTO = AnimalDTO().input_delete()
        except InputException as e:
            print(e)
            return
        try:
            res = self.animal_service.delete(ID(dto.id))
        except DeleteAnimalStartedShowError:
            print(self.lm.out_deleted_animal_active_shows_error)
            return
        print(self.lm.out_deleted_success + f' (ID: {res.id.value}, статус: {res.status})')

    def create_animal(self, user_id: int) -> None:
        try:
            dto: AnimalDTO = AnimalDTO().input_create(user_id)
        except InputException as e:
            print(e)
            return
        created = self.animal_service.create(dto.to_schema_create())
        AnimalDTO.from_schema(created).print()
        # todo: try except integrity error (wrong fk)
    #
    # def get_animals_all(self) -> None:
    #     res = self.animal_service.get_all()
    #     if len(res) == 0:
    #         print(self.lm.get_empty_result)
    #         return
    #     for animal in res:
    #         AnimalDTO.from_schema(animal).print()
