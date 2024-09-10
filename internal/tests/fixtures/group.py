import pytest

from internal.src.core.group.schema.group import GroupSchema
from internal.tests.builders.schema.group import GroupSchemaBuilder


@pytest.fixture
def group_repository(container):
    return container.group_repo()


@pytest.fixture
def groupschema() -> GroupSchema:
    return GroupSchemaBuilder().with_test_values().build()


@pytest.fixture
def group(group_repository, groupschema):
    group = group_repository.create(groupschema)
    yield group
    group_repository.delete(group.id.value)


@pytest.fixture
def created_group(group_repository, groupschema):
    return group_repository.create(groupschema)


@pytest.fixture
def invalid_group_id(group_repository, created_group):
    group_repository.delete(created_group.id.value)
    return created_group.id
    