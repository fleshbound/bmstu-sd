import datetime

import pytest
from pydantic import PositiveFloat, NonNegativeInt

from internal.tests.repository.container.container import TestRepositoryContainer
from internal.src.core.animal.schema.animal import AnimalSchema
from internal.src.core.utils.types import ID, AnimalName, Datetime, Sex, Weight, Height, Length


container = TestRepositoryContainer()


@pytest.fixture
def animal_repository():
    return container.animal_repo()


def animalschema(id: NonNegativeInt,
                 user_id: NonNegativeInt,
                 breed_id: NonNegativeInt,
                 weight: PositiveFloat,
                 length: PositiveFloat,
                 height: PositiveFloat,
                 has_defects: bool,
                 is_multicolor: bool,
                 name: str,
                 sex: Sex) -> AnimalSchema:
    return AnimalSchema(
            id=ID(id),
            user_id=ID(user_id),
            breed_id=ID(breed_id),
            name=AnimalName(name),
            birth_dt=Datetime(datetime.datetime(2020, 10, 15)),
            sex=sex,
            weight=Weight(weight),
            height=Height(height),
            has_defects=has_defects,
            is_multicolor=is_multicolor,
            length=Length(length)
    )


def test_animal_create_ok(animal_repository):
    animal = animalschema(0, 1, 1, 100, 100, 100, False, False, 'Cool Animal Name', Sex.female)
    created = animal_repository.create(animal)
    found = animal_repository.get_by_id(created.id.value)
    assert found.user_id.value == 1
    assert found.breed_id.value == 1
    assert found.weight.value == 100
    assert found.length.value == 100
    assert found.height.value == 100
    assert found.has_defects is False
    assert found.is_multicolor is False
    assert found.name.value == 'Cool Animal Name'
    assert found.sex == Sex.female
