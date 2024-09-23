from tech.handlers.input import InputHandler
from tech.utils.lang.langmodel import LanguageModel
from core.animal.service.animal import IAnimalService
from core.show.service.show import IShowService

from tech.dto.animal import AnimalDTO
from tech.utils.exceptions import InputException
from core.utils.exceptions import DeleteAnimalStartedShowError, NotFoundRepoError, ValidationRepoError
from core.utils.types import ID


class AnimalHandler:
    animal_service: IAnimalService
    show_service: IShowService
    input_handler: InputHandler
    lm: LanguageModel

    def __init__(self,
                 animal_service: IAnimalService,
                 show_service: IShowService,
                 input_handler: InputHandler):
        self.animal_service = animal_service
        self.show_service = show_service
        self.input_handler = input_handler
        self.lm = self.input_handler.lang_model

    def get_animals_by_user_id(self, user_id: int) -> None:
        try:
            res = self.animal_service.get_by_user_id(ID(user_id))
        except NotFoundRepoError:
            print(self.lm.get_empty_result)
            return
        for animal in res:
            AnimalDTO.from_schema(animal, self.input_handler).print()

    def delete_animal(self, user_id: int) -> None:
        try:
            dto: AnimalDTO = AnimalDTO(input_handler=self.input_handler).input_delete()
        except InputException:
            return

        existing_dto = self.animal_service.get_by_id(ID(dto.id))
        if existing_dto.user_id != user_id:
            print(self.lm.not_owner_error)
            return

        try:
            res = self.animal_service.delete(ID(dto.id))
        except DeleteAnimalStartedShowError:
            print(self.lm.out_deleted_animal_active_shows_error)
            return
        print(self.lm.out_deleted_success + f' (ID: {res.id.value}, статус: {res.status})')

    def create_animal(self, user_id: int) -> None:
        try:
            dto: AnimalDTO = AnimalDTO(input_handler=self.input_handler).input_create(user_id)
        except InputException :
            return
        try:
            created = self.animal_service.create(dto.to_schema_create())
        except ValidationRepoError:
            print(self.lm.foreign_keys_error)
            return
        AnimalDTO.from_schema(created, self.input_handler).print()
