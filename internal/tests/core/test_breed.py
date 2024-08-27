import pytest

from core.breed.schema.breed import BreedSchema, BreedDeleteStatus, BreedSchemaCreate, BreedSchemaUpdate
<<<<<<<< HEAD:internal/tests/core/test_breed.py
from core.breed.service.impl.breed import BreedService
|||||||| parent of a759adf (add console UI files):internal/app/tests/core/breed/test_service.py
from core.breed.service import BreedService
<<<<<<<< HEAD:internal/tests/core/test_breed.py
from internal.app.tests.core.breed.mock.repository import MockedBreedRepository
========
from core.breed.service import BreedService
from internal.petowo.tests.core.breed.mock.repository import MockedBreedRepository
>>>>>>>> a759adf (add console UI files):internal/petowo/tests/core/user/test_service.py
|||||||| parent of a759adf (add console UI files):internal/app/tests/core/user/test_service.py
from internal.app.tests.core.breed.mock.repository import MockedBreedRepository
========
from internal.petowo.tests.core.breed.mock.repository import MockedBreedRepository
>>>>>>>> a759adf (add console UI files):internal/petowo/tests/core/breed/test_service.py
from core.utils.types import ID, BreedName
from internal.tests.core.mymock.repo.breed import MockedBreedRepository


@pytest.fixture
def mocked_id():
    return ID(1)


@pytest.fixture
def mocked_skip():
    return 10


@pytest.fixture
def mocked_limit():
    return 100


@pytest.fixture
def mocked_name():
    return BreedName(value="Breed name")


@pytest.fixture
def mocked_breedschema(mocked_id, mocked_name):
    return BreedSchema(
        id=mocked_id,
        name=mocked_name,
        species_id=mocked_id
    )


@pytest.fixture
def mocked_breedschemacreate(mocked_id, mocked_name):
    return BreedSchemaCreate(
        name=mocked_name,
        species_id=mocked_id
    )


@pytest.fixture
def mocked_breedschemaupdate(mocked_id):
    return BreedSchemaUpdate(
        id=mocked_id,
        name=BreedName(value="New Breed Name")
    )


@pytest.fixture
def mocked_breed_repo(mocked_breedschema):
    return MockedBreedRepository(breeds=[mocked_breedschema])


@pytest.fixture
def breed_service(mocked_breed_repo):
    return BreedService(breed_repo=mocked_breed_repo)


def test_get_by_id_ok(breed_service, mocked_id):
    breed_service.get_by_id(mocked_id)


def test_get_all_ok(breed_service):
    breed_service.get_all()


def test_get_all_skip_limit_ok(breed_service, mocked_skip, mocked_limit):
    breed_service.get_all(skip=mocked_skip, limit=mocked_limit)


def test_delete_status_ok(breed_service, mocked_id):
    response = breed_service.delete(mocked_id)
    assert response.id == mocked_id
    assert response.status == BreedDeleteStatus.deleted


def test_create_match_ok(breed_service, mocked_breedschemacreate):
    new_breed = breed_service.create(mocked_breedschemacreate)
    assert new_breed.name == mocked_breedschemacreate.name
    assert new_breed.species_id == mocked_breedschemacreate.species_id


def test_update_match_ok(breed_service, mocked_breedschemaupdate):
    updated_breed = breed_service.update(mocked_breedschemaupdate)
    assert updated_breed.name == mocked_breedschemaupdate.name
    assert updated_breed.id == mocked_breedschemaupdate.id


def test_get_by_species_id_ok(breed_service, mocked_id):
    breed_service.get_by_species_id(mocked_id)
