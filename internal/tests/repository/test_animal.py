import pytest

from internal.src.core.utils.exceptions import NotFoundRepoError, ValidationRepoError
from internal.src.core.utils.types import ID
from internal.tests.builders.schema.animal import AnimalSchemaBuilder


@pytest.fixture
def user_id_no_animal(animal_repository, user) -> ID:
    for a in animal_repository.get_all():
        animal_repository.delete(a.id.value)
    yield user.id


@pytest.fixture
def user_id_one_animal(animal_repository, user_id_no_animal, breed):
    res = animal_repository.create(
        AnimalSchemaBuilder()
        .with_test_values()
        .with_user_id(user_id_no_animal.value)
        .with_breed_id(breed.id.value)
        .build()
    )
    return res.user_id


@pytest.fixture
def animal_updated_invalid_id(invalid_animal_id):
    return (
        AnimalSchemaBuilder()
        .with_test_values()
        .with_id(invalid_animal_id.value)
        .build()
    )


@pytest.fixture
def animal_updated_name(animal):
    return (
        AnimalSchemaBuilder()
        .from_object(animal)
        .with_name('New Cool Name')
        .build()
    )


@pytest.fixture
def animal_updated_user_id(animal, user_repository, userschema):
    return (
        AnimalSchemaBuilder()
        .from_object(animal)
        .with_user_id(user_repository.create(userschema).id.value)
        .build()
    )


@pytest.fixture
def animal_updated_breed_id(animal, breed_repository, breedschema):
    return (
        AnimalSchemaBuilder()
        .from_object(animal)
        .with_breed_id(breed_repository.create(breedschema).id.value)
        .build()
    )


@pytest.fixture
def empty_animal_repository(animal_repository):
    for a in animal_repository.get_all():
        animal_repository.delete(a.id.value)
    return animal_repository


@pytest.fixture
def two_animal_repository(empty_animal_repository, animalschema):
    empty_animal_repository.create(animalschema)
    empty_animal_repository.create(animalschema)
    return empty_animal_repository


@pytest.fixture
def animal_updated_invalid_user_id(animal, invalid_user_id):
    return (
        AnimalSchemaBuilder()
        .from_object(animal)
        .with_user_id(invalid_user_id.value)
        .build()
    )


@pytest.fixture
def animal_updated_invalid_breed_id(animal, invalid_breed_id):
    return (
        AnimalSchemaBuilder()
        .from_object(animal)
        .with_breed_id(invalid_breed_id.value)
        .build()
    )


class TestCreate:
    def test_ok(self, animal_repository, animalschema):
        created = animal_repository.create(animalschema)

        result = animal_repository.get_by_id(created.id.value)
        tmp = animalschema
        tmp.id = created.id
        assert result == tmp


class TestGetById:
    def test_ok(self, animal_repository, animal):
        found = animal_repository.get_by_id(animal.id.value)

        assert found == animal

    def test_notfound_error(self, animal_repository, invalid_animal_id: ID):
        with pytest.raises(NotFoundRepoError):
            animal_repository.get_by_id(invalid_animal_id.value)


class TestDelete:
    def test_ok(self, animal_repository, created_animal):
        animal_repository.delete(created_animal.id.value)

        with pytest.raises(NotFoundRepoError):
            animal_repository.get_by_id(created_animal.id.value)

    def test_notfound_error(self, animal_repository, invalid_animal_id: ID):
        with pytest.raises(NotFoundRepoError):
            animal_repository.delete(invalid_animal_id.value)


class TestGetByUserId:
    def test_no_animal_error(self, animal_repository, user_id_no_animal):
        with pytest.raises(NotFoundRepoError):
            animal_repository.get_by_user_id(user_id_no_animal.value)
            
    def test_one_animal_ok(self, animal_repository, user_id_one_animal):
        res = animal_repository.get_by_user_id(user_id_one_animal.value)
        
        assert len(res) == 1


class TestGetAll:
    def test_empty_len_eq_zero(self, empty_animal_repository):
        assert len(empty_animal_repository.get_all()) == 0

    def test_two_animal_len_eq_two(self, two_animal_repository):
        assert len(two_animal_repository.get_all()) == 2


class TestUpdate:
    def test_invalid_id_error(self, animal_repository, animal_updated_invalid_id):
        with pytest.raises(NotFoundRepoError):
            animal_repository.update(animal_updated_invalid_id)

    def test_update_name_ok(self, animal_repository, animal_updated_name, animal):
        res = animal_repository.update(animal_updated_name)

        assert res.name != animal.name and res.name == animal_updated_name.name
    
    def test_invalid_user_id_error(self, animal_repository, animal_updated_invalid_user_id):
        with pytest.raises(ValidationRepoError):
            animal_repository.update(animal_updated_invalid_user_id)

    def test_user_id_ok(self, animal_repository, animal, animal_updated_user_id):
        res = animal_repository.update(animal_updated_user_id)

        assert res.user_id != animal.user_id and res.user_id == animal_updated_user_id.user_id

    def test_invalid_breed_id_error(self, animal_repository, animal_updated_invalid_breed_id):
        with pytest.raises(ValidationRepoError):
            animal_repository.update(animal_updated_invalid_breed_id)

    def test_breed_id_ok(self, animal_repository, animal, animal_updated_breed_id):
        res = animal_repository.update(animal_updated_breed_id)

        assert res.breed_id != animal.breed_id and res.breed_id == animal_updated_breed_id.breed_id
