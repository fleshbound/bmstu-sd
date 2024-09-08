import pytest

from internal.src.core.utils.exceptions import NotFoundRepoError, ValidationRepoError
from internal.src.core.utils.types import ID
from internal.tests.builders.usershow import UserShowSchemaBuilder


@pytest.fixture
def user_id_no_usershow(usershow_repository, user) -> ID:
    for a in usershow_repository.get_all():
        usershow_repository.delete(a.id.value)
    yield user.id


@pytest.fixture
def user_id_one_usershow(usershow_repository, user_id_no_usershow, show):
    res = usershow_repository.create(
        UserShowSchemaBuilder()
        .with_test_values()
        .with_user_id(user_id_no_usershow.value)
        .with_show_id(show.id.value)
        .build()
    )
    return res.user_id


@pytest.fixture
def show_id_no_usershow(usershow_repository, show) -> ID:
    for a in usershow_repository.get_all():
        usershow_repository.delete(a.id.value)
    yield show.id


@pytest.fixture
def show_id_one_usershow(usershow_repository, show_id_no_usershow, user):
    res = usershow_repository.create(
        UserShowSchemaBuilder()
        .with_test_values()
        .with_user_id(user.id.value)
        .with_show_id(show_id_no_usershow.value)
        .build()
    )
    return res.show_id


@pytest.fixture
def usershow_updated_invalid_id(invalid_usershow_id):
    return (
        UserShowSchemaBuilder()
        .with_test_values()
        .with_id(invalid_usershow_id.value)
        .build()
    )


@pytest.fixture
def usershow_updated_is_archived(usershow):
    return (
        UserShowSchemaBuilder()
        .from_object(usershow)
        .with_is_archived(True)
        .build()
    )


@pytest.fixture
def usershow_updated_user_id(usershow, user_repository, userschema):
    return (
        UserShowSchemaBuilder()
        .from_object(usershow)
        .with_user_id(user_repository.create(userschema).id.value)
        .build()
    )


@pytest.fixture
def usershow_updated_show_id(usershow, show_repository, showschema):
    return (
        UserShowSchemaBuilder()
        .from_object(usershow)
        .with_show_id(show_repository.create(showschema).id.value)
        .build()
    )


@pytest.fixture
def empty_usershow_repository(usershow_repository):
    for a in usershow_repository.get_all():
        usershow_repository.delete(a.id.value)
    return usershow_repository


@pytest.fixture
def two_usershow_repository(empty_usershow_repository, usershowschema):
    empty_usershow_repository.create(usershowschema)
    empty_usershow_repository.create(usershowschema)
    return empty_usershow_repository


@pytest.fixture
def usershow_updated_invalid_user_id(usershow, invalid_user_id, show):
    return (
        UserShowSchemaBuilder()
        .from_object(usershow)
        .with_user_id(invalid_user_id.value)
        .with_show_id(show.id.value)
        .build()
    )


@pytest.fixture
def usershow_updated_invalid_show_id(usershow, invalid_show_id, user):
    return (
        UserShowSchemaBuilder()
        .from_object(usershow)
        .with_show_id(invalid_show_id.value)
        .with_user_id(user.id.value)
        .build()
    )


class TestCreate:
    def test_ok(self, usershow_repository, usershowschema):
        created = usershow_repository.create(usershowschema)

        result = usershow_repository.get_by_id(created.id.value)
        tmp = usershowschema
        tmp.id = created.id
        assert result == tmp


class TestGetById:
    def test_ok(self, usershow_repository, usershow):
        found = usershow_repository.get_by_id(usershow.id.value)

        assert found == usershow

    def test_notfound_error(self, usershow_repository, invalid_usershow_id: ID):
        with pytest.raises(NotFoundRepoError):
            usershow_repository.get_by_id(invalid_usershow_id.value)


class TestDelete:
    def test_ok(self, usershow_repository, created_usershow):
        usershow_repository.delete(created_usershow.id.value)

        with pytest.raises(NotFoundRepoError):
            usershow_repository.get_by_id(created_usershow.id.value)

    def test_notfound_error(self, usershow_repository, invalid_usershow_id: ID):
        with pytest.raises(NotFoundRepoError):
            usershow_repository.delete(invalid_usershow_id.value)


class TestGetByUserId:
    def test_no_usershow_error(self, usershow_repository, user_id_no_usershow):
        with pytest.raises(NotFoundRepoError):
            usershow_repository.get_by_user_id(user_id_no_usershow.value)

    def test_one_usershow_ok(self, usershow_repository, user_id_one_usershow):
        res = usershow_repository.get_by_user_id(user_id_one_usershow.value)

        assert len(res) == 1


class TestGetByShowId:
    def test_no_usershow_error(self, usershow_repository, show_id_no_usershow):
        with pytest.raises(NotFoundRepoError):
            usershow_repository.get_by_show_id(show_id_no_usershow.value)

    def test_one_usershow_ok(self, usershow_repository, show_id_one_usershow):
        res = usershow_repository.get_by_show_id(show_id_one_usershow.value)

        assert len(res) == 1


class TestGetAll:
    def test_empty_len_eq_zero(self, empty_usershow_repository):
        assert len(empty_usershow_repository.get_all()) == 0

    def test_two_usershow_len_eq_two(self, two_usershow_repository):
        assert len(two_usershow_repository.get_all()) == 2


class TestUpdate:
    def test_invalid_id_error(self, usershow_repository, usershow_updated_invalid_id):
        with pytest.raises(NotFoundRepoError):
            usershow_repository.update(usershow_updated_invalid_id)

    def test_update_is_archived_ok(self, usershow_repository, usershow_updated_is_archived, usershow):
        res = usershow_repository.update(usershow_updated_is_archived)

        assert res.is_archived != usershow.is_archived and res.is_archived == usershow_updated_is_archived.is_archived

    def test_invalid_user_id_error(self, usershow_repository, usershow_updated_invalid_user_id):
        with pytest.raises(ValidationRepoError):
            usershow_repository.update(usershow_updated_invalid_user_id)

    def test_user_id_ok(self, usershow_repository, usershow, usershow_updated_user_id):
        res = usershow_repository.update(usershow_updated_user_id)

        assert res.user_id != usershow.user_id and res.user_id == usershow_updated_user_id.user_id

    def test_invalid_show_id_error(self, usershow_repository, usershow_updated_invalid_show_id):
        with pytest.raises(ValidationRepoError):
            usershow_repository.update(usershow_updated_invalid_show_id)

    def test_show_id_ok(self, usershow_repository, usershow, usershow_updated_show_id):
        res = usershow_repository.update(usershow_updated_show_id)

        assert res.show_id != usershow.show_id and res.show_id == usershow_updated_show_id.show_id
