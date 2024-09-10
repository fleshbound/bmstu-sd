import pytest

from internal.src.core.utils.exceptions import NotFoundRepoError
from internal.src.core.utils.types import ID
from internal.tests.builders.schema.show import ShowSchemaBuilder


@pytest.fixture
def show_updated_invalid_id(invalid_show_id):
    return (
        ShowSchemaBuilder()
        .with_test_values()
        .with_id(invalid_show_id.value)
        .build()
    )


@pytest.fixture
def breed_id_no_show(show_repository, breed) -> ID:
    for a in show_repository.get_all():
        show_repository.delete(a.id.value)
    return breed.id


@pytest.fixture
def breed_id_one_show(show_repository, breed_id_no_show, standard):
    res = show_repository.create(
        ShowSchemaBuilder()
        .with_test_values()
        .with_breed_id(breed_id_no_show.value)
        .with_species_id(None)
        .with_standard_id(standard.id.value)
        .with_is_multi_breed(False)
        .build()
    )
    return res.breed_id


@pytest.fixture
def standard_id_no_show(show_repository, standard) -> ID:
    for a in show_repository.get_all():
        show_repository.delete(a.id.value)
    return standard.id


@pytest.fixture
def standard_id_one_show(show_repository, standard_id_no_show, breed):
    res = show_repository.create(
        ShowSchemaBuilder()
        .with_test_values()
        .with_breed_id(breed.id.value)
        .with_species_id(None)
        .with_standard_id(standard_id_no_show.value)
        .with_is_multi_breed(False)
        .build()
    )
    return res.standard_id


@pytest.fixture
def species_id_no_show(show_repository, species) -> ID:
    for a in show_repository.get_all():
        show_repository.delete(a.id.value)
    return species.id


@pytest.fixture
def species_id_one_show(show_repository, species_id_no_show, species):
    res = show_repository.create(
        ShowSchemaBuilder()
        .with_test_values()
        .with_species_id(species_id_no_show.value)
        .with_breed_id(None)
        .with_standard_id(None)
        .with_is_multi_breed(True)
        .build()
    )
    return res.species_id


@pytest.fixture
def empty_show_repository(show_repository):
    for a in show_repository.get_all():
        show_repository.delete(a.id.value)
    return show_repository


@pytest.fixture
def two_show_repository(empty_show_repository, showschema):
    empty_show_repository.create(showschema)
    empty_show_repository.create(showschema)
    return empty_show_repository


class TestGetById:
    def test_ok(self, show_repository, show):
        found = show_repository.get_by_id(show.id.value)

        assert found == show

    def test_notfound_error(self, show_repository, invalid_show_id: ID):
        with pytest.raises(NotFoundRepoError):
            show_repository.get_by_id(invalid_show_id.value)


class TestGetByBreedId:
    def test_no_show_error(self, show_repository, breed_id_no_show):
        with pytest.raises(NotFoundRepoError):
            show_repository.get_by_breed_id(breed_id_no_show.value)

    def test_one_show_ok(self, show_repository, breed_id_one_show):
        res = show_repository.get_by_breed_id(breed_id_one_show.value)

        assert len(res) == 1


class TestGetBySpeciesId:
    def test_no_show_error(self, show_repository, species_id_no_show):
        with pytest.raises(NotFoundRepoError):
            show_repository.get_by_species_id(species_id_no_show.value)

    def test_one_show_ok(self, show_repository, species_id_one_show):
        res = show_repository.get_by_species_id(species_id_one_show.value)

        assert len(res) == 1


class TestCreate:
    def test_ok(self, show_repository, showschema):
        created = show_repository.create(showschema)

        result = show_repository.get_by_id(created.id.value)
        tmp = showschema
        tmp.id = created.id
        assert result == tmp


class TestGetByStandardId:
    def test_no_show_error(self, show_repository, standard_id_no_show):
        with pytest.raises(NotFoundRepoError):
            show_repository.get_by_standard_id(standard_id_no_show.value)

    def test_one_show_ok(self, show_repository, standard_id_one_show):
        res = show_repository.get_by_standard_id(standard_id_one_show.value)

        assert len(res) == 1


class TestDelete:
    def test_ok(self, show_repository, created_show):
        show_repository.delete(created_show.id.value)

        with pytest.raises(NotFoundRepoError):
            show_repository.get_by_id(created_show.id.value)

    def test_notfound_error(self, show_repository, invalid_show_id: ID):
        with pytest.raises(NotFoundRepoError):
            show_repository.delete(invalid_show_id.value)


class TestGetAll:
    def test_empty_len_eq_zero(self, empty_show_repository):
        res_len = len(empty_show_repository.get_all())
        assert res_len == 0, f'Result length was {res_len}, should be 0'

    def test_two_show_len_eq_two(self, two_show_repository):
        res_len = len(two_show_repository.get_all())
        assert res_len == 2, f'Result length was {res_len}, should be 2'
