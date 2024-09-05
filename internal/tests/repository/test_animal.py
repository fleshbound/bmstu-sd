import datetime

import pytest
from pydantic import PositiveFloat, NonNegativeInt

from internal.src.repository.sqlalchemy.animal import SqlAlchemyAnimalRepository
from internal.tests.builders.animal import AnimalSchemaBuilder
from internal.src.core.group.schema.group import GroupSchema
from internal.src.core.species.schema.species import SpeciesSchema
from internal.src.core.user.schema.user import UserSchema, UserRole

from internal.src.core.breed.schema.breed import BreedSchema
from internal.src.core.utils.exceptions import NotFoundRepoError
from internal.tests.repository.container.container import RepositoryContainer
from internal.src.core.animal.schema.animal import AnimalSchema
from internal.src.core.utils.types import ID, AnimalName, Datetime, Sex, Weight, Height, Length, UserName, Email, \
    HashedPassword, GroupName, SpeciesName, BreedName

container = RepositoryContainer()


@pytest.fixture
def animal_repository():
    return container.animal_repo()


@pytest.fixture
def user_repository():
    return container.user_repo()


@pytest.fixture
def species_repository():
    return container.species_repo()


@pytest.fixture
def breed_repository():
    return container.breed_repo()


@pytest.fixture
def group_repository():
    return container.group_repo()


@pytest.fixture
def mocked_user(user_repository):
    user = user_repository.create(UserSchema(
        id=ID(0),
        email=Email('coolemail@gmail.com'),
        hashed_password=HashedPassword('coolpass'),
        role=UserRole.breeder,
        name=UserName('Cool Bob')
    ))
    yield user
    user_repository.delete(user.id.value)


@pytest.fixture
def mocked_group(group_repository):
    group = group_repository.create(GroupSchema(id=ID(0), name=GroupName('Cool Group')))
    yield group
    group_repository.delete(group.id.value)


@pytest.fixture
def mocked_species(species_repository, mocked_group):
    species = species_repository.create(SpeciesSchema(id=ID(0), name=SpeciesName('Cool Species'),
                                                      group_id=mocked_group.id))
    yield species
    species_repository.delete(species.id.value)


@pytest.fixture
def mocked_breed(breed_repository, mocked_species):
    breed = breed_repository.create(
        BreedSchema(id=ID(0), name=BreedName('Cool Breed'), species_id=mocked_species.id))
    yield breed
    breed_repository.delete(breed.id.value)


@pytest.fixture
def animalschema(mocked_user, mocked_breed) -> AnimalSchema:
    return AnimalSchemaBuilder().with_test_values().build()


@pytest.fixture
def animal(animal_repository: SqlAlchemyAnimalRepository, animalschema) -> AnimalSchema:
    res_animal = animal_repository.create(animalschema)
    yield res_animal
    animal_repository.delete(res_animal.id.value)


@pytest.fixture
def created_animal(animal_repository: SqlAlchemyAnimalRepository, animalschema) -> AnimalSchema:
    res_animal = animal_repository.create(animalschema)
    return res_animal


@pytest.fixture
def invalid_animal_id(animal_repository: SqlAlchemyAnimalRepository, created_animal) -> ID:
    animal_repository.delete(created_animal.id)
    return created_animal.id


class TestCreate:
    def test_ok(self, animal_repository: SqlAlchemyAnimalRepository, animalschema: AnimalSchema):
        created = animal_repository.create(animalschema)

        result = animal_repository.get_by_id(created.id.value)
        tmp = animalschema
        tmp.id = created.id
        assert result == tmp


class TestGetById:
    def test_ok(self, animal_repository: SqlAlchemyAnimalRepository, animal: AnimalSchema):
        found = animal_repository.get_by_id(animal.id.value)
        assert found == animal

    def test_notfound_error(self, animal_repository: SqlAlchemyAnimalRepository, invalid_animal_id: ID):
        with pytest.raises(NotFoundRepoError):
            animal_repository.get_by_id(invalid_animal_id.value)


class TestDelete:
    def test_ok(self, animal_repository: SqlAlchemyAnimalRepository, created_animal: AnimalSchema):
        animal_repository.delete(created_animal.id.value)

        with pytest.raises(NotFoundRepoError):
            animal_repository.get_by_id(created_animal.id.value)

    def test_notfound_error(self, animal_repository: SqlAlchemyAnimalRepository, invalid_animal_id: ID):
        with pytest.raises(NotFoundRepoError):
            animal_repository.delete(invalid_animal_id.value)
