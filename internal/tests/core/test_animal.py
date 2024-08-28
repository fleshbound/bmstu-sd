import datetime

import pytest

from internal.src.core.animal.schema.animal import AnimalSchema
from internal.src.core.animal.service.impl.animal import AnimalService
from internal.src.core.utils.types import ID, AnimalName, Datetime, Sex, Weight, Height, Length
from internal.tests.core.mock.repo.animal import MockedAnimalRepository
from internal.tests.core.mock.service.animalshow import MockedAnimalShowService
from internal.tests.core.mock.service.show import MockedShowService


@pytest.fixture
def mocked_animalschema():
    return AnimalSchema(
            id=ID(0),
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


def test_delete_noanimalshow_ok(mocked_animalschema):
    id = mocked_animalschema.id
    animal_service = AnimalService(
        animal_repo=MockedAnimalRepository(animals=[mocked_animalschema]),
        animalshow_service=MockedAnimalShowService([]),
        show_service=MockedShowService([])
    )
    assert animal_service.delete(id).id == id
