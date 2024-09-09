import pytest

from internal.src.core.utils.exceptions import NotFoundRepoError, ValidationRepoError
from internal.src.core.utils.types import ID
from builders.schema.animalshow import AnimalShowSchemaBuilder


@pytest.fixture
def animal_id_no_animalshow(animalshow_repository, animal) -> ID:
    for a in animalshow_repository.get_all():
        animalshow_repository.delete(a.id.value)
    yield animal.id


@pytest.fixture
def animal_id_one_animalshow(animalshow_repository, animal_id_no_animalshow, show):
    res = animalshow_repository.create(
        AnimalShowSchemaBuilder()
        .with_test_values()
        .with_animal_id(animal_id_no_animalshow.value)
        .with_show_id(show.id.value)
        .build()
    )
    return res.animal_id


@pytest.fixture
def show_id_no_animalshow(animalshow_repository, show) -> ID:
    for a in animalshow_repository.get_all():
        animalshow_repository.delete(a.id.value)
    yield show.id


@pytest.fixture
def show_id_one_animalshow(animalshow_repository, show_id_no_animalshow, animal):
    res = animalshow_repository.create(
        AnimalShowSchemaBuilder()
        .with_test_values()
        .with_animal_id(animal.id.value)
        .with_show_id(show_id_no_animalshow.value)
        .build()
    )
    return res.show_id


@pytest.fixture
def animalshow_updated_invalid_id(invalid_animalshow_id):
    return (
        AnimalShowSchemaBuilder()
        .with_test_values()
        .with_id(invalid_animalshow_id.value)
        .build()
    )


@pytest.fixture
def animalshow_updated_is_archived(animalshow):
    return (
        AnimalShowSchemaBuilder()
        .from_object(animalshow)
        .with_is_archived(True)
        .build()
    )


@pytest.fixture
def animalshow_updated_animal_id(animalshow, animal_repository, animalschema):
    return (
        AnimalShowSchemaBuilder()
        .from_object(animalshow)
        .with_animal_id(animal_repository.create(animalschema).id.value)
        .build()
    )


@pytest.fixture
def animalshow_updated_show_id(animalshow, show_repository, showschema):
    return (
        AnimalShowSchemaBuilder()
        .from_object(animalshow)
        .with_show_id(show_repository.create(showschema).id.value)
        .build()
    )


@pytest.fixture
def empty_animalshow_repository(animalshow_repository):
    for a in animalshow_repository.get_all():
        animalshow_repository.delete(a.id.value)
    return animalshow_repository


@pytest.fixture
def two_animalshow_repository(empty_animalshow_repository, animalshowschema):
    empty_animalshow_repository.create(animalshowschema)
    empty_animalshow_repository.create(animalshowschema)
    return empty_animalshow_repository


@pytest.fixture
def animalshow_updated_invalid_animal_id(animalshow, invalid_animal_id, show):
    return (
        AnimalShowSchemaBuilder()
        .from_object(animalshow)
        .with_show_id(show.id.value)
        .with_animal_id(invalid_animal_id.value)
        .build()
    )


@pytest.fixture
def animalshow_updated_invalid_show_id(animalshow, invalid_show_id, animal):
    return (
        AnimalShowSchemaBuilder()
        .from_object(animalshow)
        .with_show_id(invalid_show_id.value)
        .with_animal_id(animal.id.value)
        .build()
    )


class TestCreate:
    def test_ok(self, animalshow_repository, animalshowschema):
        created = animalshow_repository.create(animalshowschema)

        result = animalshow_repository.get_by_id(created.id.value)
        tmp = animalshowschema
        tmp.id = created.id
        assert result == tmp


class TestGetById:
    def test_ok(self, animalshow_repository, animalshow):
        found = animalshow_repository.get_by_id(animalshow.id.value)

        assert found == animalshow

    def test_notfound_error(self, animalshow_repository, invalid_animalshow_id: ID):
        with pytest.raises(NotFoundRepoError):
            animalshow_repository.get_by_id(invalid_animalshow_id.value)


class TestDelete:
    def test_ok(self, animalshow_repository, created_animalshow):
        animalshow_repository.delete(created_animalshow.id.value)

        with pytest.raises(NotFoundRepoError):
            animalshow_repository.get_by_id(created_animalshow.id.value)

    def test_notfound_error(self, animalshow_repository, invalid_animalshow_id: ID):
        with pytest.raises(NotFoundRepoError):
            animalshow_repository.delete(invalid_animalshow_id.value)


class TestGetByAnimalId:
    def test_no_animalshow_error(self, animalshow_repository, animal_id_no_animalshow):
        with pytest.raises(NotFoundRepoError):
            animalshow_repository.get_by_animal_id(animal_id_no_animalshow.value)

    def test_one_animalshow_ok(self, animalshow_repository, animal_id_one_animalshow):
        res = animalshow_repository.get_by_animal_id(animal_id_one_animalshow.value)

        assert len(res) == 1


class TestGetByShowId:
    def test_no_animalshow_error(self, animalshow_repository, show_id_no_animalshow):
        with pytest.raises(NotFoundRepoError):
            animalshow_repository.get_by_show_id(show_id_no_animalshow.value)

    def test_one_animalshow_ok(self, animalshow_repository, show_id_one_animalshow):
        res = animalshow_repository.get_by_show_id(show_id_one_animalshow.value)

        assert len(res) == 1


class TestGetAll:
    def test_empty_len_eq_zero(self, empty_animalshow_repository):
        assert len(empty_animalshow_repository.get_all()) == 0

    def test_two_animalshow_len_eq_two(self, two_animalshow_repository):
        assert len(two_animalshow_repository.get_all()) == 2


class TestUpdate:
    def test_invalid_id_error(self, animalshow_repository, animalshow_updated_invalid_id):
        with pytest.raises(NotFoundRepoError):
            animalshow_repository.update(animalshow_updated_invalid_id)

    def test_update_is_archived_ok(self, animalshow_repository, animalshow_updated_is_archived, animalshow):
        res = animalshow_repository.update(animalshow_updated_is_archived)

        assert (res.is_archived != animalshow.is_archived and
                res.is_archived == animalshow_updated_is_archived.is_archived)

    def test_invalid_animal_id_error(self, animalshow_repository, animalshow_updated_invalid_animal_id):
        with pytest.raises(ValidationRepoError):
            animalshow_repository.update(animalshow_updated_invalid_animal_id)

    def test_animal_id_ok(self, animalshow_repository, animalshow, animalshow_updated_animal_id):
        res = animalshow_repository.update(animalshow_updated_animal_id)

        assert res.animal_id != animalshow.animal_id and res.animal_id == animalshow_updated_animal_id.animal_id

    def test_invalid_show_id_error(self, animalshow_repository, animalshow_updated_invalid_show_id):
        with pytest.raises(ValidationRepoError):
            animalshow_repository.update(animalshow_updated_invalid_show_id)

    def test_show_id_ok(self, animalshow_repository, animalshow, animalshow_updated_show_id):
        res = animalshow_repository.update(animalshow_updated_show_id)

        assert res.show_id != animalshow.show_id and res.show_id == animalshow_updated_show_id.show_id
