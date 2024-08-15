import pytest

from core.species.schema.species import SpeciesSchema, SpeciesDeleteStatus, SpeciesSchemaCreate, SpeciesSchemaUpdate
from core.species.service.impl.species import SpeciesService
from internal.tests.core.species.mock.repository import MockedSpeciesRepository
from core.utils.types import ID, SpeciesName


@pytest.fixture
def mocked_id():
    return ID(value=1)


@pytest.fixture
def mocked_skip():
    return 10


@pytest.fixture
def mocked_limit():
    return 100


@pytest.fixture
def mocked_name():
    return SpeciesName(value="Species name")


@pytest.fixture
def mocked_speciesschema(mocked_id, mocked_name):
    return SpeciesSchema(
        id=mocked_id,
        name=mocked_name,
        group_id=mocked_id
    )


@pytest.fixture
def mocked_speciesschemacreate(mocked_id, mocked_name):
    return SpeciesSchemaCreate(
        name=mocked_name,
        group_id=mocked_id
    )


@pytest.fixture
def mocked_speciesschemaupdate(mocked_id):
    return SpeciesSchemaUpdate(
        id=mocked_id,
        name=SpeciesName(value="New Species Name")
    )


@pytest.fixture
def mocked_species_repo(mocked_speciesschema):
    return MockedSpeciesRepository(speciess=[mocked_speciesschema])


@pytest.fixture
def species_service(mocked_species_repo):
    return SpeciesService(species_repo=mocked_species_repo)


def test_get_by_id_ok(species_service, mocked_id):
    species_service.get_by_id(mocked_id)


def test_get_all_ok(species_service):
    species_service.get_all()


def test_get_all_skip_limit_ok(species_service, mocked_skip, mocked_limit):
    species_service.get_all(skip=mocked_skip, limit=mocked_limit)


def test_delete_status_ok(species_service, mocked_id):
    response = species_service.delete(mocked_id)
    assert response.id == mocked_id
    assert response.status == SpeciesDeleteStatus.deleted


def test_create_match_ok(species_service, mocked_speciesschemacreate):
    new_species = species_service.create(mocked_speciesschemacreate)
    assert new_species.name == mocked_speciesschemacreate.name
    assert new_species.group_id == mocked_speciesschemacreate.group_id


def test_update_match_ok(species_service, mocked_speciesschemaupdate):
    updated_species = species_service.update(mocked_speciesschemaupdate)
    assert updated_species.name == mocked_speciesschemaupdate.name
    assert updated_species.id == mocked_speciesschemaupdate.id


def test_get_by_group_id_ok(species_service, mocked_id):
    species_service.get_by_group_id(mocked_id)
