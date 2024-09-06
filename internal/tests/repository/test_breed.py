import pytest

from internal.tests.builders.group import GroupSchemaBuilder
from internal.src.core.group.schema.group import GroupSchema
from internal.tests.builders.species import SpeciesSchemaBuilder
from internal.src.core.species.schema.species import SpeciesSchema
from internal.tests.builders.breed import BreedSchemaBuilder
from internal.src.core.breed.schema.breed import BreedSchema
from internal.src.core.utils.exceptions import NotFoundRepoError, ValidationRepoError
from internal.src.core.utils.types import ID
from internal.tests.repository.container.container import RepositoryContainer


@pytest.fixture
def container():
    return RepositoryContainer()


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
def species_repository(container):
    return container.species_repo()


@pytest.fixture
def species(species_repository, speciesschema):
    species = species_repository.create(speciesschema)
    yield species
    species_repository.delete(species.id.value)


@pytest.fixture
def speciesschema(group) -> SpeciesSchema:
    return SpeciesSchemaBuilder().with_test_values().with_group_id(group.id.value).build()


@pytest.fixture
def created_species(species_repository, speciesschema):
    return species_repository.create(speciesschema)


@pytest.fixture
def invalid_species_id(species_repository, created_species):
    species_repository.delete(created_species.id.value)
    return created_species.id


@pytest.fixture
def breed_updated_invalid_id(invalid_breed_id):
    return (
        BreedSchemaBuilder()
        .with_test_values()
        .with_id(invalid_breed_id.value)
        .build()
    )


@pytest.fixture
def empty_breed_repository(breed_repository):
    for a in breed_repository.get_all():
        breed_repository.delete(a.id.value)
    return breed_repository


@pytest.fixture
def two_breed_repository(empty_breed_repository, breedschema):
    empty_breed_repository.create(breedschema)
    empty_breed_repository.create(breedschema)
    return empty_breed_repository


@pytest.fixture
def breed_updated_name(breed):
    return (
        BreedSchemaBuilder()
        .from_object(breed)
        .with_name('New Cool Breed Name')
        .build()
    )


@pytest.fixture
def breed_updated_species_id(species_repository, speciesschema, breed):
    return (
        BreedSchemaBuilder()
        .from_object(breed)
        .with_species_id(species_repository.create(speciesschema).id.value)
        .with_name('New Cool Breed Name')
        .build()
    )


@pytest.fixture
def breed_updated_invalid_species_id(breed, invalid_species_id):
    return (
        BreedSchemaBuilder()
        .from_object(breed)
        .with_species_id(invalid_species_id.value)
        .build()
    )


class TestCreate:
    def test_ok(self, breed_repository, breedschema):
        created = breed_repository.create(breedschema)

        result = breed_repository.get_by_id(created.id.value)
        tmp = breedschema
        tmp.id = created.id
        assert result == tmp


class TestGetById:
    def test_ok(self, breed_repository, breed):
        found = breed_repository.get_by_id(breed.id.value)

        assert found == breed

    def test_notfound_error(self, breed_repository, invalid_breed_id: ID):
        with pytest.raises(NotFoundRepoError):
            breed_repository.get_by_id(invalid_breed_id.value)


class TestDelete:
    def test_ok(self, breed_repository, created_breed):
        breed_repository.delete(created_breed.id.value)

        with pytest.raises(NotFoundRepoError):
            breed_repository.get_by_id(created_breed.id.value)

    def test_notfound_error(self, breed_repository, invalid_breed_id: ID):
        with pytest.raises(NotFoundRepoError):
            breed_repository.delete(invalid_breed_id.value)


class TestGetAll:
    def test_empty_len_eq_zero(self, empty_breed_repository):
        assert len(empty_breed_repository.get_all()) == 0

    def test_two_breed_len_eq_two(self, two_breed_repository):
        assert len(two_breed_repository.get_all()) == 2


class TestUpdate:
    def test_invalid_id_error(self, breed_repository, breed_updated_invalid_id):
        with pytest.raises(NotFoundRepoError):
            breed_repository.update(breed_updated_invalid_id)

    def test_update_name_ok(self, breed_repository, breed_updated_name, breed):
        res = breed_repository.update(breed_updated_name)

        assert res.name != breed.name and res.name == breed_updated_name.name

    def test_invalid_species_id_error(self, breed_repository, breed_updated_invalid_species_id):
        with pytest.raises(ValidationRepoError):
            breed_repository.update(breed_updated_invalid_species_id)

    def test_species_id_ok(self, breed_repository, breed, breed_updated_species_id):
        res = breed_repository.update(breed_updated_species_id)

        assert (res.species_id != breed.species_id and res.species_id == breed_updated_species_id.species_id)
