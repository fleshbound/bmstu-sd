import pytest

from internal.tests.builders.group import GroupSchemaBuilder
from internal.src.core.group.schema.group import GroupSchema
from internal.src.core.utils.exceptions import NotFoundRepoError
from internal.src.core.utils.types import ID
from internal.tests.repository.container.container import RepositoryContainer


@pytest.fixture
def container():
    return RepositoryContainer()


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


@pytest.fixture
def group_updated_invalid_id(invalid_group_id):
    return (
        GroupSchemaBuilder()
        .with_test_values()
        .with_id(invalid_group_id.value)
        .build()
    )


@pytest.fixture
def empty_group_repository(group_repository):
    for a in group_repository.get_all():
        group_repository.delete(a.id.value)
    return group_repository


@pytest.fixture
def two_group_repository(empty_group_repository, groupschema):
    empty_group_repository.create(groupschema)
    empty_group_repository.create(groupschema)
    return empty_group_repository


@pytest.fixture
def group_updated_name(group):
    return (
        GroupSchemaBuilder()
        .from_object(group)
        .with_name('New Cool Group Name')
        .build()
    )


class TestCreate:
    def test_ok(self, group_repository, groupschema):
        created = group_repository.create(groupschema)

        result = group_repository.get_by_id(created.id.value)
        tmp = groupschema
        tmp.id = created.id
        assert result == tmp


class TestGetById:
    def test_ok(self, group_repository, group):
        found = group_repository.get_by_id(group.id.value)

        assert found == group

    def test_notfound_error(self, group_repository, invalid_group_id: ID):
        with pytest.raises(NotFoundRepoError):
            group_repository.get_by_id(invalid_group_id.value)


class TestDelete:
    def test_ok(self, group_repository, created_group):
        group_repository.delete(created_group.id.value)

        with pytest.raises(NotFoundRepoError):
            group_repository.get_by_id(created_group.id.value)

    def test_notfound_error(self, group_repository, invalid_group_id: ID):
        with pytest.raises(NotFoundRepoError):
            group_repository.delete(invalid_group_id.value)


class TestGetAll:
    def test_empty_len_eq_zero(self, empty_group_repository):
        assert len(empty_group_repository.get_all()) == 0

    def test_two_group_len_eq_two(self, two_group_repository):
        assert len(two_group_repository.get_all()) == 2


class TestUpdate:
    def test_invalid_id_error(self, group_repository, group_updated_invalid_id):
        with pytest.raises(NotFoundRepoError):
            group_repository.update(group_updated_invalid_id)

    def test_update_name_ok(self, group_repository, group_updated_name, group):
        res = group_repository.update(group_updated_name)

        assert res.name != group.name and res.name == group_updated_name.name
