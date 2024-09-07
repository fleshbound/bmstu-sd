import pytest

from internal.src.core.breed.schema.breed import BreedSchema
from internal.tests.builders.breed import BreedSchemaBuilder


@pytest.fixture
def breed_repository(container):
    return container.breed_repo()


@pytest.fixture
def breedschema(species) -> BreedSchema:
    return BreedSchemaBuilder().with_test_values().with_species_id(species.id.value).build()


@pytest.fixture
def breed(breed_repository, breedschema):
    breed = breed_repository.create(breedschema)
    yield breed
    breed_repository.delete(breed.id.value)


@pytest.fixture
def created_breed(breed_repository, breedschema):
    return breed_repository.create(breedschema)


@pytest.fixture
def invalid_breed_id(breed_repository, created_breed):
    breed_repository.delete(created_breed.id.value)
    return created_breed.id

