import logging

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
        logging.info(f'animal handler: get animals by user_id, user_id={user_id}')
        try:
            res = self.animal_service.get_by_user_id(ID(user_id))
        except NotFoundRepoError:
            logging.warning(f'animal handler: empty output animals by user_id={user_id}')
            print(self.lm.get_empty_result)
            return
        for animal in res:
            AnimalDTO.from_schema(animal, self.input_handler).print()

    def delete_animal(self, user_id: int) -> None:
        logging.info(f'animal handler: delete animal, user_id={user_id}')
        try:
            dto: AnimalDTO = AnimalDTO(input_handler=self.input_handler).input_delete()
        except InputException:
            logging.warning(f'animal handler: delete animal: invalid input')
            return

        existing_dto = AnimalDTO.from_schema(self.animal_service.get_by_id(ID(dto.id)), input_handler=self.input_handler)
        if existing_dto.user_id != user_id:
            logging.warning(f'animal handler: user isn\'t animal\'s owner, user_id={user_id} animal.user_id={existing_dto.user_id}')
            print(self.lm.not_owner_error)
            return

        try:
            res = self.animal_service.delete(ID(dto.id))
        except DeleteAnimalStartedShowError:
            logging.warning(f'animal handler: delete animal error: wrong show_status')
            print(self.lm.out_deleted_animal_active_shows_error)
            return
        print(self.lm.out_deleted_success + f' (ID: {res.id.value}, статус: {res.status})')

    def create_animal(self, user_id: int) -> None:
        logging.info(f'animal handler: create animal, user_id={user_id}')
        try:
            dto: AnimalDTO = AnimalDTO(input_handler=self.input_handler).input_create(user_id)
        except InputException:
            logging.warning(f'animal handler: create animal: invalid input')
            return
        try:
            created = self.animal_service.create(dto.to_schema_create())
        except ValidationRepoError:
            logging.warning(f'animal handler: create animal: repo validation error')
            print(self.lm.foreign_keys_error)
            return
        AnimalDTO.from_schema(created, self.input_handler).print()
