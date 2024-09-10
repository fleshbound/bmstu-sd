from internal.console.tech.utils.lang.langmodel import LanguageModel
from internal.src.core.animal.service.animal import IAnimalService
from internal.src.core.show.service.show import IShowService
from internal.src.core.utils.exceptions import NotFoundRepoError

from internal.src.core.utils.types import ID


class AnimalHandler:
    animal_service: IAnimalService
    show_service: IShowService

    def __init__(self,
                 animal_service: IAnimalService,
                 show_service: IShowService,
                 lang_model: LanguageModel):
        self.animal_service = animal_service
        self.show_service = show_service
        self.lang_model = lang_model

    def delete_animal(self):
        raise NotImplementedError

    def create_animal(self):
        raise NotImplementedError

    def get_animals_by_user_id(self, user_id: ID):
        try:
            res = self.animal_service.get_by_user_id(user_id)
        except NotFoundRepoError:
            print(self.lang_model.get_animals_empty_result)
        else:
            for animal in res:


