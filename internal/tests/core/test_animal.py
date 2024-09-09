import datetime
from typing import Optional, List

import pytest
from pydantic import NonNegativeInt

from internal.src.core.animal.schema.animal import AnimalSchema
from internal.src.core.animal.service.impl.animal import AnimalService
from internal.src.core.show.schema.animalshow import AnimalShowSchema
from internal.src.core.show.schema.show import ShowStatus, ShowSchema, ShowClass
from internal.src.core.utils.exceptions import DeleteAnimalStartedShowError
from internal.src.core.utils.types import ID, AnimalName, Datetime, Sex, Weight, Height, Length, ShowName, Country
from internal.tests.core.mymock.repo.animal import MockedAnimalRepository
from internal.tests.core.mymock.service.animalshow import MockedAnimalShowService
from internal.tests.core.mymock.service.show import MockedShowService


def mocked_animalschema(id: NonNegativeInt) -> AnimalSchema:
    return AnimalSchema(
            id=ID(id),
            user_id=ID(0),
            breed_id=ID(0),
            name=AnimalName('Cool Animal Name'),
            birth_dt=Datetime(datetime.datetime(2020, 10, 15)),
            sex=Sex.male,
            weight=Weight(1.1),
            height=Height(1.1),
            length=Length(1.1),
            has_defects=True,
            is_multicolor=False
    )


# @pytest.fixture
# def animal_service():
#     return AnimalService


def animal_service_create(animals: List[AnimalSchema], animalshows: List[AnimalShowSchema], shows: List[ShowSchema]):
    return AnimalService(
        animal_repo=MockedAnimalRepository(animals=animals),
        animalshow_service=MockedAnimalShowService(animalshows=animalshows),
        show_service=MockedShowService(shows, animalshows, [], animals, [])
    )


def mocked_animalshowschema(id: NonNegativeInt = 0,
                            animal_id: NonNegativeInt = 0,
                            show_id: NonNegativeInt = 0,
                            is_archived: bool = False):
    return AnimalShowSchema(id=ID(id), animal_id=ID(animal_id), show_id=ID(show_id), is_archived=is_archived)


def mocked_showschema(id: NonNegativeInt = 0,
                      status: ShowStatus = ShowStatus.created,
                      species_id: Optional[NonNegativeInt] = None,
                      breed_id: Optional[NonNegativeInt] = 0,
                      standard_id: Optional[NonNegativeInt] = 0,
                      is_multi_breed: bool = False):
    standard_id = standard_id if standard_id is None else ID(standard_id)
    species_id = species_id if species_id is None else ID(species_id)
    breed_id = breed_id if breed_id is None else ID(breed_id)
    return ShowSchema(
        id=ID(id),
        status=status,
        name=ShowName('Cool Show Name'),
        species_id=species_id,
        breed_id=breed_id,
        country=Country('Russian Federation'),
        show_class=ShowClass.one,
        standard_id=standard_id,
        is_multi_breed=is_multi_breed
    )

    
#
#
# class TestDelete:
#     def test_no_animalshow_ok(self, ):
#


def test_delete_noanimalshow_ok():
    animals = [mocked_animalschema(0)]
    animal_service = animal_service_create(animals=animals, animalshows=[], shows=[])
    assert animal_service.delete(animals[0].id).id == ID(0)


def test_delete_animalshowstarted_error():
    animals = [mocked_animalschema(id=0)]
    shows = [mocked_showschema(id=0, status=ShowStatus.started)]
    animalshows = [mocked_animalshowschema(0, 0, 0)]
    animal_service = animal_service_create(animals=animals, animalshows=animalshows, shows=shows)
    with pytest.raises(DeleteAnimalStartedShowError):
        animal_service.delete(ID(0))


def test_delete_animalshowcreated_ok():
    animals = [mocked_animalschema(id=0)]
    shows = [mocked_showschema(0, ShowStatus.created)]
    animalshows = [mocked_animalshowschema(0, 0, 0)]
    animal_service = animal_service_create(animals=animals, animalshows=animalshows, shows=shows)
    assert animal_service.delete(animals[0].id).id == animals[0].id
