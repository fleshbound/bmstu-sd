import datetime
from typing import List, Optional

import pytest
from pydantic import NonNegativeInt

from core.animal.schema.animal import AnimalSchema
from core.show.schema.animalshow import AnimalShowSchema
from core.show.schema.score import ScoreSchema
from core.show.schema.show import ShowSchema, ShowClass, ShowStatus
from core.show.schema.usershow import UserShowSchema
from core.show.service.impl.score import ScoreService
from core.user.schema.user import UserSchema, UserRole
from core.utils.exceptions import ScoreServiceError
from core.utils.types import ID, Datetime, ShowName, Country, HashedPassword, Email, UserName, ScoreValue
from internal.tests.core.mymock.repo.score import MockedScoreRepository
from internal.tests.core.mymock.service.animalshow import MockedAnimalShowService
from internal.tests.core.mymock.service.show import MockedShowService
from internal.tests.core.mymock.service.usershow import MockedUserShowService


def score_service_create(scores: List[ScoreSchema],
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
                       value: NonNegativeInt,
                       is_archived: bool):
    return ScoreSchema(
            id=ID(id),
            value=ScoreValue(value),
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


def test_get_show_ranking_info_one_animal():
    scores = [mocked_scoreschema(0, 0, 0, 5, False),
              mocked_scoreschema(0, 1, 0, 0, False)]
    animalshows = [mocked_animalshowschema(0, 0,             0, False)]
    score_service = score_service_create(scores, [], animalshows, [], [], [])
    count, res = score_service.get_show_ranking_info(ID(0))
    assert count == 1
    assert res[0].rank == 1
    assert res[0].total_info.average == 2.5


def test_get_show_ranking_info_two_not_equal():
    scores = [mocked_scoreschema(0, 0, 0, 5, False),
              mocked_scoreschema(1, 1, 0, 0, False),
              mocked_scoreschema(2, 0, 1, 4, False),
              mocked_scoreschema(3, 1, 1, 4, False)]
    animalshows = [mocked_animalshowschema(0, 0, 0, False),
                   mocked_animalshowschema(1, 1, 0, False)]
    score_service = score_service_create(scores, [], animalshows, [], [], [])
    count, res = score_service.get_show_ranking_info(ID(0))
    assert count == 2
    assert res[0].rank == 1 and res[0].total_info.record_id.value == 1
    assert res[1].rank == 2 and res[1].total_info.record_id.value == 0
    assert res[0].total_info.average == 4
    assert res[1].total_info.average == 2.5
    assert res[0].total_info.max_score.value == 4 and res[0].total_info.min_score.value == 4
    assert res[1].total_info.max_score.value == 5 and res[1].total_info.min_score.value == 0


def test_get_show_ranking_info_two_equal():
    scores = [mocked_scoreschema(0, 0, 0, 5, False),
              mocked_scoreschema(1, 1, 0, 0, False),
              mocked_scoreschema(2, 0, 1, 0, False),
              mocked_scoreschema(3, 1, 1, 5, False)]
    animalshows = [mocked_animalshowschema(0, 0, 0, False),
                   mocked_animalshowschema(1, 1, 0, False)]
    score_service = score_service_create(scores, [], animalshows, [], [], [])
    count, res = score_service.get_show_ranking_info(ID(0))
    assert count == 1
    assert len(res) == 2
    assert res[0].rank == 1 and res[0].total_info.record_id.value == 0
    assert res[1].rank == 1 and res[1].total_info.record_id.value == 1
    assert res[0].total_info.average == 2.5
    assert res[1].total_info.average == 2.5
    assert res[0].total_info.max_score.value == 5 and res[0].total_info.min_score.value == 0
    assert res[1].total_info.max_score.value == 5 and res[1].total_info.min_score.value == 0


def test_get_show_ranking_info_avg_zero():
    scores = [mocked_scoreschema(0, 0, 0, 0, False),
              mocked_scoreschema(1, 1, 0, 0, False)]
    animalshows = [mocked_animalshowschema(0, 0, 0, False)]
    score_service = score_service_create(scores, [], animalshows, [], [], [])
    count, res = score_service.get_show_ranking_info(ID(0))
    assert count == 1
    assert len(res) == 1
    assert res[0].rank == 1 and res[0].total_info.record_id.value == 0
    assert res[0].total_info.average == 0
    assert res[0].total_info.max_score.value == 0 and res[0].total_info.min_score.value == 0


def test_get_show_ranking_info_no_scores_error():
    scores = []
    animalshows = [mocked_animalshowschema(0, 0, 0, False)]
    score_service = score_service_create(scores, [], animalshows, [], [], [])
    with pytest.raises(ScoreServiceError):
        score_service.get_show_ranking_info(ID(0))
