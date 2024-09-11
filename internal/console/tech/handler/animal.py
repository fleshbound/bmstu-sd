from core.animal.service.animal import IAnimalService
from core.show.service.show import IShowService


class AnimalHandler:
    animal_service: IAnimalService
    show_service: IShowService

    def __init__(self,
                 animal_service: IAnimalService,
                 show_service: IShowService):
        self.animal_service = animal_service
        self.show_service = show_service

    def delete_animal(self):
        raise

    def create_animal(self):
        raise NotImplementedError

    def get_animals_all(self):
        raise

