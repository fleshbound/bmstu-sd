import pytest

from core.group.schema.group import GroupSchema, GroupDeleteStatus, GroupSchemaCreate, GroupSchemaUpdate
from core.group.service.impl.group import GroupService
from core.utils.types import ID, GroupName
from internal.tests.core.mymock.repo.group import MockedGroupRepository


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
    return GroupName(value="Group name")


@pytest.fixture
def mocked_groupschema(mocked_id, mocked_name):
    return GroupSchema(
        id=mocked_id,
        name=mocked_name
    )


@pytest.fixture
def mocked_groupschemacreate(mocked_id, mocked_name):
    return GroupSchemaCreate(
        name=mocked_name
    )


@pytest.fixture
def mocked_groupschemaupdate(mocked_id):
    return GroupSchemaUpdate(
        id=mocked_id,
        name=GroupName(value="New Group Name")
    )


@pytest.fixture
def mocked_group_repo(mocked_groupschema):
    return MockedGroupRepository(groups=[mocked_groupschema])


@pytest.fixture
def group_service(mocked_group_repo):
    return GroupService(group_repo=mocked_group_repo)


def test_get_by_id_ok(group_service, mocked_id):
    group_service.get_by_id(mocked_id)


def test_get_all_ok(group_service):
    group_service.get_all()


def test_get_all_skip_limit_ok(group_service, mocked_skip, mocked_limit):
    group_service.get_all(skip=mocked_skip, limit=mocked_limit)


def test_delete_status_ok(group_service, mocked_id):
    response = group_service.delete(mocked_id)
    assert response.id == mocked_id
    assert response.status == GroupDeleteStatus.deleted


def test_create_match_ok(group_service, mocked_groupschemacreate):
    new_group = group_service.create(mocked_groupschemacreate)
    assert new_group.name == mocked_groupschemacreate.name


def test_update_match_ok(group_service, mocked_groupschemaupdate):
    updated_group = group_service.update(mocked_groupschemaupdate)
    assert updated_group.name == mocked_groupschemaupdate.name
    assert updated_group.id == mocked_groupschemaupdate.id
