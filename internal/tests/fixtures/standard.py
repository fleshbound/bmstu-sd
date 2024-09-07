import pytest

from internal.src.core.standard.schema.standard import StandardSchema
from internal.src.core.utils.types import ID
from internal.tests.builders.standard import StandardSchemaBuilder


@pytest.fixture
def standard_repository(container):
    return container.standard_repo()


@pytest.fixture
def standardschema(breed) -> StandardSchema:
    return (
        StandardSchemaBuilder()
        .with_test_values()
        .with_breed_id(breed.id.value)
        .build()
    )


@pytest.fixture
def standard(standard_repository, standardschema) -> StandardSchema:
    res_standard = standard_repository.create(standardschema)
    yield res_standard
    standard_repository.delete(res_standard.id.value)


@pytest.fixture
def created_standard(standard_repository, standardschema) -> StandardSchema:
    res_standard = standard_repository.create(standardschema)
    return res_standard


@pytest.fixture
def invalid_standard_id(standard_repository, created_standard) -> ID:
    standard_repository.delete(created_standard.id.value)
    return created_standard.id
