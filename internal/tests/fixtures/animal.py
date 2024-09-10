import pytest

from internal.src.core.animal.schema.animal import AnimalSchema
from internal.src.core.utils.types import ID
from internal.tests.builders.schema.animal import AnimalSchemaBuilder


@pytest.fixture
def animal_repository(container):
    return container.animal_repo()


@pytest.fixture
def animalschema(user, breed) -> AnimalSchema:
    return (
        AnimalSchemaBuilder()
        .with_test_values()
        .with_user_id(user.id.value)
        .with_breed_id(breed.id.value)
        .build()
    )


@pytest.fixture
def animal(animal_repository, animalschema) -> AnimalSchema:
    res_animal = animal_repository.create(animalschema)
    yield res_animal
    animal_repository.delete(res_animal.id.value)


@pytest.fixture
def created_animal(animal_repository, animalschema) -> AnimalSchema:
    res_animal = animal_repository.create(animalschema)
    return res_animal


@pytest.fixture
def invalid_animal_id(animal_repository, created_animal) -> ID:
    animal_repository.delete(created_animal.id.value)
    return created_animal.id
