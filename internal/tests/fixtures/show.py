import pytest

from internal.src.core.show.schema.show import ShowSchema
from internal.tests.builders.show import ShowSchemaBuilder


@pytest.fixture
def show_repository(container):
    return container.show_repo()


@pytest.fixture
def showschema(breed, standard) -> ShowSchema:
    return (
        ShowSchemaBuilder()
        .with_test_values()
        .with_breed_id(breed.id.value)
        .with_species_id(None)
        .with_is_multi_breed(False)
        .with_standard_id(standard.id.value)
        .build()
    )


@pytest.fixture
def show(show_repository, showschema) -> ShowSchema:
    res_show = show_repository.create(showschema)
    yield res_show
    show_repository.delete(res_show.id.value)


@pytest.fixture
def created_show(show_repository, showschema):
    return show_repository.create(showschema)


@pytest.fixture
def invalid_show_id(show_repository, created_show):
    show_repository.delete(created_show.id.value)
    return created_show.id