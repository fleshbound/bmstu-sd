import pytest

from internal.src.core.utils.exceptions import NotFoundRepoError
from internal.src.core.utils.types import ID
from builders.schema.standard import StandardSchemaBuilder


@pytest.fixture
def standard_updated_invalid_id(invalid_standard_id):
    return (
        StandardSchemaBuilder()
        .with_test_values()
        .with_id(invalid_standard_id.value)
        .build()
    )


@pytest.fixture
def standard_updated_name(standard):
    return (
        StandardSchemaBuilder()
        .from_object(standard)
        .with_name('New Cool Name')
        .build()
    )


@pytest.fixture
def standard_updated_breed_id(standard, breed_repository, breedschema):
    return (
        StandardSchemaBuilder()
        .from_object(standard)
        .with_breed_id(breed_repository.create(breedschema).id.value)
        .build()
    )


@pytest.fixture
def empty_standard_repository(standard_repository):
    for a in standard_repository.get_all():
        standard_repository.delete(a.id.value)
    return standard_repository


@pytest.fixture
def two_standard_repository(empty_standard_repository, standardschema):
    empty_standard_repository.create(standardschema)
    empty_standard_repository.create(standardschema)
    return empty_standard_repository


@pytest.fixture
def invalid_breed_id(breed_repository, created_breed):
    breed_repository.delete(created_breed.id.value)
    return created_breed.id


@pytest.fixture
def standard_updated_invalid_breed_id(standard, invalid_breed_id):
    return (
        StandardSchemaBuilder()
        .from_object(standard)
        .with_breed_id(invalid_breed_id.value)
        .build()
    )


@pytest.fixture
def breed_id_no_standard(standard_repository, breed) -> ID:
    for s in standard_repository.get_all():
        standard_repository.delete(s.id.value)
    yield breed.id
    

@pytest.fixture
def breed_id_one_standard(standard_repository, breed_id_no_standard):
    return standard_repository.create(
        StandardSchemaBuilder()
        .with_test_values()
        .with_breed_id(breed_id_no_standard.value)
        .build()
    ).breed_id


class TestCreate:
    def test_ok(self, standard_repository, standardschema):
        created = standard_repository.create(standardschema)

        result = standard_repository.get_by_id(created.id.value)
        tmp = standardschema
        tmp.id = created.id
        assert result == tmp


class TestGetById:
    def test_ok(self, standard_repository, standard):
        found = standard_repository.get_by_id(standard.id.value)

        assert found == standard

    def test_notfound_error(self, standard_repository, invalid_standard_id: ID):
        with pytest.raises(NotFoundRepoError):
            standard_repository.get_by_id(invalid_standard_id.value)


class TestDelete:
    def test_ok(self, standard_repository, created_standard):
        standard_repository.delete(created_standard.id.value)

        with pytest.raises(NotFoundRepoError):
            standard_repository.get_by_id(created_standard.id.value)

    def test_notfound_error(self, standard_repository, invalid_standard_id: ID):
        with pytest.raises(NotFoundRepoError):
            standard_repository.delete(invalid_standard_id.value)


class TestGetByBreedId:
    def test_no_standard_error(self, standard_repository, breed):
        with pytest.raises(NotFoundRepoError) as excinfo:
            standard_repository.get_by_breed_id(breed.id.value)

        assert 'not found by breed_id' in str(excinfo.value)

    def test_one_standard_ok(self, standard_repository, breed_id_one_standard):
        res_len = len(standard_repository.get_by_breed_id(breed_id_one_standard.value))

        assert res_len == 1, f'Result length was {res_len}, should be 1'


class TestGetAll:
    def test_empty_len_eq_zero(self, empty_standard_repository):
        res_len = len(empty_standard_repository.get_all())
        assert res_len == 0, f'Result length was {res_len}, should be 0'

    def test_two_standard_len_eq_two(self, two_standard_repository):
        res_len = len(two_standard_repository.get_all())
        assert res_len == 2, f'Result length was {res_len}, should be 2'
