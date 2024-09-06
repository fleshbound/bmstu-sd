import pytest

from internal.src.core.animal.schema.animal import AnimalSchema
from internal.src.core.group.schema.group import GroupSchema
from internal.src.core.user.schema.user import UserSchema
from internal.src.core.utils.exceptions import NotFoundRepoError, ValidationRepoError
from internal.src.core.utils.types import ID
from internal.tests.builders.animal import AnimalSchemaBuilder
from internal.tests.builders.breed import BreedSchemaBuilder
from internal.tests.builders.group import GroupSchemaBuilder
from internal.tests.builders.species import SpeciesSchemaBuilder
from internal.tests.builders.user import UserSchemaBuilder
from internal.tests.repository.container.container import RepositoryContainer


@pytest.fixture
def container():
    return RepositoryContainer()


@pytest.fixture
def animal_repository(container):
    return container.animal_repo()


@pytest.fixture
def user_repository(container):
    return container.user_repo()


@pytest.fixture
def species_repository(container):
    return container.species_repo()


@pytest.fixture
def breed_repository(container):
    return container.breed_repo()


@pytest.fixture
def group_repository(container):
    return container.group_repo()


@pytest.fixture
def userschema() -> UserSchema:
    return UserSchemaBuilder().with_test_values().build()


@pytest.fixture
def user(user_repository, userschema):
    user = user_repository.create(userschema)
    yield user
    user_repository.delete(user.id.value)


@pytest.fixture
def created_user(user_repository, userschema):
    return user_repository.create(userschema)


@pytest.fixture
def groupschema() -> GroupSchema:
    return GroupSchemaBuilder().with_test_values().build()


@pytest.fixture
def group(group_repository, groupschema):
    group = group_repository.create(groupschema)
    yield group
    group_repository.delete(group.id.value)


@pytest.fixture
def speciesschema(group):
    return SpeciesSchemaBuilder().with_test_values().with_group_id(group.id.value).build()


@pytest.fixture
def species(species_repository, speciesschema):
    species = species_repository.create(speciesschema)
    yield species
    species_repository.delete(species.id.value)


@pytest.fixture
def breedschema(species):
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
def animalschema(user, breed) -> AnimalSchema:
    return (
        AnimalSchemaBuilder()
        .with_test_values()
        .with_user_id(user.id.value)
        .with_breed_id(breed.id.value)
        .build()
    )


@pytest.fixture
def animal(animal_repository, animalschema) -> AnimalSchema:
    res_animal = animal_repository.create(animalschema)
    yield res_animal
    animal_repository.delete(res_animal.id.value)


@pytest.fixture
def created_animal(animal_repository, animalschema) -> AnimalSchema:
    res_animal = animal_repository.create(animalschema)
    return res_animal


@pytest.fixture
def invalid_animal_id(animal_repository, created_animal) -> ID:
    animal_repository.delete(created_animal.id.value)
    return created_animal.id


@pytest.fixture
def user_id_no_animal(animal_repository, user, created_animal) -> ID:
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
def invalid_user_id(user_repository, created_user):
    user_repository.delete(created_user.id.value)
    return created_user.id


@pytest.fixture
def invalid_breed_id(breed_repository, created_breed):
    breed_repository.delete(created_breed.id.value)
    return created_breed.id


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
            print(animal_repository.get_by_user_id(user_id_no_animal.value))
            
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
