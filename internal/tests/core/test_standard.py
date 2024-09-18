import datetime
from typing import List, Optional

import pytest
from pydantic import NonNegativeInt, PositiveFloat

from core.animal.schema.animal import AnimalSchema
from core.show.schema.show import ShowStatus, ShowSchema, ShowClass
from core.standard.schema.standard import StandardSchema
from core.standard.service.impl.standard import StandardService
from core.utils.exceptions import CheckAnimalStandardError, StandardInUseError, CheckAnimalBreedError
from core.utils.types import ID, Country, Weight, Height, Length, AnimalName, Datetime, Sex, ShowName
from internal.tests.core.mymock.repo.standard import MockedStandardRepository
from internal.tests.core.mymock.service.show import MockedShowService


def mocked_standardschema(breed_id: NonNegativeInt,
                          weight: PositiveFloat,
                          length: PositiveFloat,
                          height: PositiveFloat,
                          has_defects: bool,
                          is_multicolor: bool,
                          weight_delta_percent: PositiveFloat,
                          height_delta_percent: PositiveFloat,
                          length_delta_percent: PositiveFloat) -> StandardSchema:
    return StandardSchema(
        id=ID(0),
        breed_id=ID(breed_id),
        country=Country('Russian Federation'),
        weight=Weight(weight),
        height=Height(height),
        has_defects=has_defects,
        is_multicolor=is_multicolor,
        length=Length(length),
        weight_delta_percent=weight_delta_percent,
        height_delta_percent=height_delta_percent,
        length_delta_percent=length_delta_percent
    )


def mocked_animalschema(breed_id: NonNegativeInt,
                        weight: PositiveFloat,
                        length: PositiveFloat,
                        height: PositiveFloat,
                        has_defects: bool,
                        is_multicolor: bool) -> AnimalSchema:
    return AnimalSchema(
            id=ID(0),
            user_id=ID(0),
            breed_id=ID(breed_id),
            name=AnimalName('Cool Animal Name'),
            birth_dt=Datetime(datetime.datetime(2020, 10, 15)),
            sex=Sex.male,
            weight=Weight(weight),
            height=Height(height),
            has_defects=has_defects,
            is_multicolor=is_multicolor,
            length=Length(length)
    )


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


def standard_service_create(standards: List[StandardSchema], shows: List[ShowSchema]):
    return StandardService(standard_repo=MockedStandardRepository(standards=standards),
                           show_service=MockedShowService(shows, [], [], [], []))


def test_check_wrongbreed_error():
    standards = [mocked_standardschema(0, 1, 1, 1, True, True, 10, 10, 10)]
    animal = mocked_animalschema(1, 1, 1, 1, True, True)
    standard_service = standard_service_create(standards, [])
    with pytest.raises(CheckAnimalBreedError):
        standard_service.check_animal_by_standard(ID(0), animal)


def test_check_moreweight_false():
    standards = [mocked_standardschema(0, 100, 1, 1, True, True, 10, 10, 10)]
    animal = mocked_animalschema(0, 89, 1, 1, True, True)
    standard_service = standard_service_create(standards, [])
    with pytest.raises(CheckAnimalStandardError):
        standard_service.check_animal_by_standard(ID(0), animal)


def test_check_lessweight_false():
    standards = [mocked_standardschema(0, 100, 1, 1, True, True, 10, 10, 10)]
    animal = mocked_animalschema(0, 111, 1, 1, True, True)
    standard_service = standard_service_create(standards, [])
    with pytest.raises(CheckAnimalStandardError):
        standard_service.check_animal_by_standard(ID(0), animal)


def test_check_lesslength_false():
    standards = [mocked_standardschema(0, 100, 100, 1, True, True, 10, 10, 10)]
    animal = mocked_animalschema(0, 100, 89, 1, True, True)
    standard_service = standard_service_create(standards, [])
    with pytest.raises(CheckAnimalStandardError):
        standard_service.check_animal_by_standard(ID(0), animal)


def test_check_morelength_false():
    standards = [mocked_standardschema(0, 100, 100, 1, True, True, 10, 10, 10)]
    animal = mocked_animalschema(0, 100, 111, 1, True, True)
    standard_service = standard_service_create(standards, [])
    with pytest.raises(CheckAnimalStandardError):
        standard_service.check_animal_by_standard(ID(0), animal)


def test_check_lessheight_false():
    standards = [mocked_standardschema(0, 100, 100, 100, True, True, 10, 10, 10)]
    animal = mocked_animalschema(0, 100, 100, 89, True, True)
    standard_service = standard_service_create(standards, [])
    with pytest.raises(CheckAnimalStandardError):
        standard_service.check_animal_by_standard(ID(0), animal)


def test_check_moreheight_false():
    standards = [mocked_standardschema(0, 100, 100, 100, True, True, 10, 10, 10)]
    animal = mocked_animalschema(0, 100, 100, 111, True, True)
    standard_service = standard_service_create(standards, [])
    with pytest.raises(CheckAnimalStandardError):
        standard_service.check_animal_by_standard(ID(0), animal)


def test_check_hasdefects_false():
    standards = [mocked_standardschema(0, 100, 100, 100, False, True, 10, 10, 10)]
    animal = mocked_animalschema(0, 100, 100, 100, True, True)
    standard_service = standard_service_create(standards, [])
    with pytest.raises(CheckAnimalStandardError):
        standard_service.check_animal_by_standard(ID(0), animal)


def test_check_ismulticolor_false():
    standards = [mocked_standardschema(0, 100, 100, 100, True, False, 10, 10, 10)]
    animal = mocked_animalschema(0, 100, 100, 100, True, True)
    standard_service = standard_service_create(standards, [])
    with pytest.raises(CheckAnimalStandardError):
        standard_service.check_animal_by_standard(ID(0), animal)


def test_check_allok_true():
    standards = [mocked_standardschema(0, 100, 100, 100, True, True, 10, 10, 10)]
    animal = mocked_animalschema(0, 100, 100, 100, True, True)
    standard_service = standard_service_create(standards, [])
    assert standard_service.check_animal_by_standard(ID(0), animal) is True


def test_delete_inuse_error():
    standards = [mocked_standardschema(0, 100, 100, 100, True, True, 10, 10, 10)]
    shows = [mocked_showschema(id=0, standard_id=0)]
    standard_service = standard_service_create(standards, shows)
    with pytest.raises(StandardInUseError):
        standard_service.delete(ID(0))


def test_delete_nouse_ok():
    standards = [mocked_standardschema(0, 100, 100, 100, True, True, 10, 10, 10)]
    shows = []
    standard_service = standard_service_create(standards, shows)
    assert standard_service.delete(ID(0)).id == ID(0)
