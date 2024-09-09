import pytest

from internal.src.core.utils.exceptions import NotFoundRepoError, ValidationRepoError
from internal.src.core.utils.types import ID
from builders.schema.species import SpeciesSchemaBuilder


@pytest.fixture
def species_updated_invalid_id(invalid_species_id):
    return (
        SpeciesSchemaBuilder()
        .with_test_values()
        .with_id(invalid_species_id.value)
        .build()
    )


@pytest.fixture
def empty_species_repository(species_repository):
    for a in species_repository.get_all():
        species_repository.delete(a.id.value)
    return species_repository


@pytest.fixture
def two_species_repository(empty_species_repository, speciesschema):
    empty_species_repository.create(speciesschema)
    empty_species_repository.create(speciesschema)
    return empty_species_repository


@pytest.fixture
def species_updated_name(species):
    return (
        SpeciesSchemaBuilder()
        .from_object(species)
        .with_name('New Cool Species Name')
        .build()
    )


@pytest.fixture
def species_updated_group_id(group_repository, groupschema, species):
    return (
        SpeciesSchemaBuilder()
        .from_object(species)
        .with_group_id(group_repository.create(groupschema).id.value)
        .with_name('New Cool Species Name')
        .build()
    )


@pytest.fixture
def species_updated_invalid_group_id(species, invalid_group_id):
    return (
        SpeciesSchemaBuilder()
        .from_object(species)
        .with_group_id(invalid_group_id.value)
        .build()
    )


class TestCreate:
    def test_ok(self, species_repository, speciesschema):
        created = species_repository.create(speciesschema)

        result = species_repository.get_by_id(created.id.value)
        tmp = speciesschema
        tmp.id = created.id
        assert result == tmp


class TestGetById:
    def test_ok(self, species_repository, species):
        found = species_repository.get_by_id(species.id.value)

        assert found == species

    def test_notfound_error(self, species_repository, invalid_species_id: ID):
        with pytest.raises(NotFoundRepoError):
            species_repository.get_by_id(invalid_species_id.value)


class TestDelete:
    def test_ok(self, species_repository, created_species):
        species_repository.delete(created_species.id.value)

        with pytest.raises(NotFoundRepoError):
            species_repository.get_by_id(created_species.id.value)

    def test_notfound_error(self, species_repository, invalid_species_id: ID):
        with pytest.raises(NotFoundRepoError):
            species_repository.delete(invalid_species_id.value)


class TestGetAll:
    def test_empty_len_eq_zero(self, empty_species_repository):
        assert len(empty_species_repository.get_all()) == 0

    def test_two_species_len_eq_two(self, two_species_repository):
        assert len(two_species_repository.get_all()) == 2


class TestUpdate:
    def test_invalid_id_error(self, species_repository, species_updated_invalid_id):
        with pytest.raises(NotFoundRepoError):
            species_repository.update(species_updated_invalid_id)

    def test_update_name_ok(self, species_repository, species_updated_name, species):
        res = species_repository.update(species_updated_name)

        assert res.name != species.name and res.name == species_updated_name.name
        
    def test_invalid_group_id_error(self, species_repository, species_updated_invalid_group_id):
        with pytest.raises(ValidationRepoError):
            species_repository.update(species_updated_invalid_group_id)

    def test_group_id_ok(self, species_repository, species, species_updated_group_id):
        res = species_repository.update(species_updated_group_id)

        assert (res.group_id != species.group_id and res.group_id == species_updated_group_id.group_id)
