import pytest

from internal.src.core.show.schema.animalshow import AnimalShowSchema
from internal.src.core.utils.types import ID
from internal.tests.builders.animalshow import AnimalShowSchemaBuilder


@pytest.fixture
def animalshow_repository(container):
    return container.animalshow_repo()


@pytest.fixture
def animalshowschema(show, animal) -> AnimalShowSchema:
    return (
        AnimalShowSchemaBuilder()
        .with_test_values()
        .with_show_id(show.id.value)
        .with_animal_id(animal.id.value)
        .build()
    )


@pytest.fixture
def animalshow(animalshow_repository, animalshowschema) -> AnimalShowSchema:
    res_animalshow = animalshow_repository.create(animalshowschema)
    yield res_animalshow
    animalshow_repository.delete(res_animalshow.id.value)


@pytest.fixture
def created_animalshow(animalshow_repository, animalshowschema) -> AnimalShowSchema:
    res_animalshow = animalshow_repository.create(animalshowschema)
    return res_animalshow


@pytest.fixture
def invalid_animalshow_id(animalshow_repository, created_animalshow) -> ID:
    animalshow_repository.delete(created_animalshow.id.value)
    return created_animalshow.id
