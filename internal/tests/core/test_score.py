import datetime
from typing import List, Optional

from pydantic import NonNegativeInt

from internal.tests.core.mock.repo.score import MockedScoreRepository
from internal.tests.core.mock.service.animalshow import MockedAnimalShowService
from internal.tests.core.mock.service.show import MockedShowService
from internal.tests.core.mock.service.usershow import MockedUserShowService
from internal.src.core.animal.schema.animal import AnimalSchema
from internal.src.core.show.schema.animalshow import AnimalShowSchema
from internal.src.core.show.schema.score import ScoreSchema, ScoreValue
from internal.src.core.show.schema.show import ShowSchema, ShowClass, ShowStatus
from internal.src.core.show.schema.usershow import UserShowSchema
from internal.src.core.show.service.impl.score import ScoreService
from internal.src.core.user.schema.user import UserSchema, UserRole
from internal.src.core.utils.types import ID, Datetime, ShowName, Country, HashedPassword, Email, UserName


def score_service(scores: List[ScoreSchema],
                  shows: List[ShowSchema],
                  animalshows: List[AnimalShowSchema],
                  usershows: List[UserShowSchema],
                  animals: List[AnimalSchema],
                  users: List[UserSchema]):
    return ScoreService(MockedShowService(shows, animalshows, usershows, animals, users),
                        MockedScoreRepository(scores),
                        MockedAnimalShowService(animalshows),
                        MockedUserShowService(usershows))


def mocked_scoreschema(id: NonNegativeInt,
                       usershow_id: NonNegativeInt,
                       animalshow_id: NonNegativeInt,
                       value: ScoreValue,
                       is_archived: bool):
    return ScoreSchema(
            id=ID(id),
            value=value,
            dt_created=Datetime(datetime.datetime(2020, 5, 10)),
            usershow_id=ID(usershow_id),
            animalshow_id=ID(animalshow_id),
            is_archived=is_archived
    )


def mocked_showschema(id: NonNegativeInt = 0,
                      status: ShowStatus = ShowStatus.created,
                      species_id: Optional[NonNegativeInt] = None,
                      breed_id: Optional[NonNegativeInt] = 0,
                      standard_id: Optional[NonNegativeInt] = 0,
                      is_multi_breed: bool = False):
    return ShowSchema(
        id=ID(id),
        status=status,
        name=ShowName('Cool Show Name'),
        species_id=ID(species_id),
        breed_id=ID(breed_id),
        country=Country('Russian Federation'),
        show_class=ShowClass.one,
        standard_id=ID(standard_id),
        is_multi_breed=is_multi_breed
    )


def mocked_userschema(id: NonNegativeInt, role: UserRole):
    return UserSchema(
            id=ID(id),
            email=Email('coolemail@gmail.com'),
            hashed_password=HashedPassword('coolpass'),
            role=role,
            name=UserName('Cool Bob')
        )


def mocked_usershowschema(id: NonNegativeInt,
                          user_id: NonNegativeInt,
                          show_id: NonNegativeInt,
                          is_archived: bool):
    return UserShowSchema(
        id=ID(id),
        user_id=ID(user_id),
        show_id=ID(show_id),
        is_archived=is_archived
    )


def mocked_animalshowschema(id: NonNegativeInt,
                            animal_id: NonNegativeInt,
                            show_id: NonNegativeInt,
                            is_archived: bool):
    return AnimalShowSchema(
        id=ID(id),
        animal_id=ID(animal_id),
        show_id=ID(show_id),
        is_archived=is_archived
    )


def test_get_total_by_usershow_id_():
    pass
