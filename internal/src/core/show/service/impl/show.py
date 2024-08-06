from typing import List

from core.show.schema.show import ShowSchemaCreate, ShowSchema, ShowSchemaUpdate, ShowSchemaDetailed, \
    ShowRegisterAnimalResult
from core.show.service.show import IShowService
from utils.types import ID


class ShowService(IShowService):
    def create(self, show_create: ShowSchemaCreate) -> ShowSchema:
        raise NotImplementedError

    def start(self, show_id: ID) -> ShowSchema:
        raise NotImplementedError

    def abort(self, show_id: ID) -> ShowSchema:
        raise NotImplementedError

    def stop(self, show_id: ID) -> ShowSchema:
        raise NotImplementedError

    def update(self, show_update: ShowSchemaUpdate) -> ShowSchema:
        raise NotImplementedError

    def get_all(self) -> List[ShowSchema]:
        raise NotImplementedError

    def get_by_id(self, show_id: ID) -> ShowSchema:
        raise NotImplementedError

    def get_by_user_id(self, user_id: ID) -> ShowSchema:
        raise NotImplementedError

    def get_by_animal_id(self, animal_id: ID) -> ShowSchema:
        raise NotImplementedError

    def get_by_id_detailed_animals(self) -> ShowSchemaDetailed:
        raise NotImplementedError

    def get_by_id_detailed_users(self) -> ShowSchemaDetailed:
        raise NotImplementedError

    def register_animal(self, animal_id: ID, show_id: ID) -> ShowRegisterAnimalResult:
        raise NotImplementedError
