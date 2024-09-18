import pytest

from core.species.schema.species import SpeciesSchema
from internal.tests.builders.schema.species import SpeciesSchemaBuilder


@pytest.fixture
def species_repository(container):
    return container.species_repo()


@pytest.fixture
def speciesschema(group) -> SpeciesSchema:
    return SpeciesSchemaBuilder().with_test_values().with_group_id(group.id.value).build()


@pytest.fixture
def species(species_repository, speciesschema):
    species = species_repository.create(speciesschema)
    yield species
    species_repository.delete(species.id.value)


@pytest.fixture
def created_species(species_repository, speciesschema):
    return species_repository.create(speciesschema)


@pytest.fixture
def invalid_species_id(species_repository, created_species):
    species_repository.delete(created_species.id.value)
    return created_species.id
