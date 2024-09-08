from typing import List

from pydantic import NonNegativeInt, PositiveInt

from internal.src.core.animal.schema.animal import AnimalSchema
from internal.src.core.show.schema.animalshow import AnimalShowSchema
from internal.src.core.show.schema.show import ShowSchemaCreate, ShowSchema, ShowSchemaUpdate, ShowSchemaDetailed, \
    ShowRegisterAnimalResult, ShowRegisterUserResult, ShowStatus, ShowClass, ShowRegisterAnimalStatus, \
    ShowRegisterUserStatus
from internal.src.core.show.schema.usershow import UserShowSchema
from internal.src.core.show.service.show import IShowService
from internal.src.core.user.schema.user import UserSchema
from internal.src.core.utils.exceptions import NotFoundRepoError
from internal.src.core.utils.types import ID, ShowName, Country


class MockedShowService(IShowService):
    _shows: List[ShowSchema]
    _animalshows: List[AnimalShowSchema]
    _usershows: List[UserShowSchema]
    _animals: List[AnimalSchema]
    _users: List[UserSchema]

    def __init__(self, shows: List[ShowSchema],
                 animalshows: List[AnimalShowSchema],
                 usershows: List[UserShowSchema],
                 animals: List[AnimalSchema],
                 users: List[UserSchema]):
        self._shows = shows
        self._animalshows = animalshows
        self._users = users
        self._animals = animals
        self._usershows = usershows

    def create(self, show_create: ShowSchemaCreate) -> ShowSchema:
        self._shows.append(ShowSchema.from_create(show_create))
        if len(self._shows) > 0:
            self._shows[-1].id = ID(len(self._shows) - 1)
        else:
            self._shows[-1].id = ID(0)
        return self._shows[-1]

    def start(self, show_id: ID) -> ShowSchema:
        for show in self._shows:
            if show.id == show_id:
                show.status = ShowStatus.started
                return show
        return ShowSchema(
            id=show_id,
            status=ShowStatus.started,
            name=ShowName('Cool Show Name'),
            species_id=None,
            breed_id=ID(0),
            country=Country('Russian Federation'),
            show_class=ShowClass.one,
            standard_id=ID(0),
            is_multi_breed=False
        )

    def abort(self, show_id: ID) -> ShowSchema:
        for show in self._shows:
            if show.id == show_id:
                show.status = ShowStatus.aborted
                return show
        return ShowSchema(
            id=show_id,
            status=ShowStatus.aborted,
            name=ShowName('Cool Show Name'),
            species_id=None,
            breed_id=ID(0),
            country=Country('Russian Federation'),
            show_class=ShowClass.one,
            standard_id=ID(0),
            is_multi_breed=False
        )

    def stop(self, show_id: ID) -> ShowSchema:
        for show in self._shows:
            if show.id == show_id:
                show.status = ShowStatus.stopped
                return show
        return ShowSchema(
            id=show_id,
            status=ShowStatus.stopped,
            name=ShowName('Cool Show Name'),
            species_id=None,
            breed_id=ID(0),
            country=Country('Russian Federation'),
            show_class=ShowClass.one,
            standard_id=ID(0),
            is_multi_breed=False
        )

    def update(self, show_update: ShowSchemaUpdate) -> ShowSchema:
        return ShowSchema(
            status=ShowStatus.stopped,
            name=ShowName('Cool Show Name'),
            species_id=None,
            breed_id=ID(0),
            country=Country('Russian Federation'),
            show_class=ShowClass.one,
            standard_id=ID(0),
            is_multi_breed=False
        ).from_update(show_update)

    def get_all(self, skip: NonNegativeInt = 0, limit: PositiveInt = 100) -> List[ShowSchema]:
        return self._shows

    def get_by_id(self, show_id: ID) -> ShowSchema:
        for show in self._shows:
            if show.id == show_id:
                return show
        raise NotFoundRepoError(detail='')

    def get_by_standard_id(self, standard_id: ID) -> List[ShowSchema]:
        res = []
        for show in self._shows:
            if show.standard_id == standard_id:
                res.append(show)
        if len(res) == 0:
            raise NotFoundRepoError(detail='')
        return res

    def get_by_user_id(self, user_id: ID) -> List[ShowSchema]:
        res = []
        for record in self._usershows:
            if record.user_id == user_id:
                for show in self._shows:
                    if show.id == record.show_id:
                        res.append(show)
        if len(res) == 0:
            raise NotFoundRepoError(detail='')
        return res
        # return [
        #     ShowSchema(
        #         id=ID(0),
        #         status=ShowStatus.created,
        #         name=ShowName('Cool Show Name'),
        #         species_id=None,
        #         breed_id=ID(0),
        #         country=Country('Russian Federation'),
        #         show_class=ShowClass.one,
        #         standard_id=ID(0),
        #         is_multi_breed=False
        #     )
        # ]

    def get_by_animal_id(self, animal_id: ID) -> List[ShowSchema]:
        res = []
        for record in self._animalshows:
            if record.animal_id == animal_id:
                for show in self._shows:
                    if show.id == record.show_id:
                        res.append(show)
        if len(res) == 0:
            raise NotFoundRepoError(detail='')
        return res
        # return [
        #     ShowSchema(
        #         id=ID(0),
        #         status=ShowStatus.created,
        #         name=ShowName('Cool Show Name'),
        #         species_id=None,
        #         breed_id=ID(0),
        #         country=Country('Russian Federation'),
        #         show_class=ShowClass.one,
        #         standard_id=ID(0),
        #         is_multi_breed=False
        #     )
        # ]

    def get_by_id_detailed(self, show_id: ID) -> ShowSchemaDetailed:
        return ShowSchemaDetailed(
                id=show_id,
                status=ShowStatus.created,
                name=ShowName('Cool Show Name'),
                species_id=None,
                breed_id=ID(0),
                country=Country('Russian Federation'),
                show_class=ShowClass.one,
                standard_id=ID(0),
                is_multi_breed=False,
                animals=[],
                users=[]
            )

    def register_animal(self, animal_id: ID, show_id: ID) -> ShowRegisterAnimalResult:
        return ShowRegisterAnimalResult(
            record_id=ID(0),
            status=ShowRegisterAnimalStatus.register_ok
        )

    def register_user(self, user_id: ID, show_id: ID) -> ShowRegisterUserResult:
        return ShowRegisterUserResult(
            record_id=ID(0),
            status=ShowRegisterUserStatus.register_ok
        )

    def unregister_animal(self, animal_id: ID, show_id: ID) -> ShowRegisterAnimalResult:
        return ShowRegisterAnimalResult(
            record_id=ID(0),
            status=ShowRegisterAnimalStatus.unregister_ok
        )

    def unregister_user(self, user_id: ID, show_id: ID) -> ShowRegisterUserResult:
        return ShowRegisterUserResult(
            record_id=ID(0),
            status=ShowRegisterUserStatus.unregister_ok
        )
    