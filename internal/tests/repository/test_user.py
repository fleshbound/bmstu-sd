import pytest

from internal.tests.builders.user import UserSchemaBuilder
from internal.src.core.user.schema.user import UserSchema
from internal.src.core.utils.exceptions import NotFoundRepoError
from internal.src.core.utils.types import ID, Email
from internal.tests.repository.container.container import RepositoryContainer


@pytest.fixture
def container():
    return RepositoryContainer()


@pytest.fixture
def user_repository(container):
    return container.user_repo()


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
def invalid_user_id(user_repository, created_user):
    user_repository.delete(created_user.id.value)
    return created_user.id


@pytest.fixture
def invalid_user_email(user_repository, created_user):
    user_repository.delete(created_user.id.value)
    return created_user.email


@pytest.fixture
def user_updated_invalid_id(invalid_user_id):
    return (
        UserSchemaBuilder()
        .with_test_values()
        .with_id(invalid_user_id.value)
        .build()
    )


@pytest.fixture
def empty_user_repository(user_repository):
    for a in user_repository.get_all():
        user_repository.delete(a.id.value)
    return user_repository


@pytest.fixture
def two_user_repository(empty_user_repository, userschema):
    empty_user_repository.create(userschema)
    empty_user_repository.create(userschema)
    return empty_user_repository


@pytest.fixture
def user_updated_name(user):
    return (
        UserSchemaBuilder()
        .from_object(user)
        .with_name('New Cool User Name')
        .build()
    )


class TestCreate:
    def test_ok(self, user_repository, userschema):
        created = user_repository.create(userschema)

        result = user_repository.get_by_id(created.id.value)
        tmp = userschema
        tmp.id = created.id
        assert result == tmp


class TestGetById:
    def test_ok(self, user_repository, user):
        found = user_repository.get_by_id(user.id.value)

        assert found == user

    def test_notfound_error(self, user_repository, invalid_user_id: ID):
        with pytest.raises(NotFoundRepoError):
            user_repository.get_by_id(invalid_user_id.value)


class TestDelete:
    def test_ok(self, user_repository, created_user):
        user_repository.delete(created_user.id.value)

        with pytest.raises(NotFoundRepoError):
            user_repository.get_by_id(created_user.id.value)

    def test_notfound_error(self, user_repository, invalid_user_id: ID):
        with pytest.raises(NotFoundRepoError):
            user_repository.delete(invalid_user_id.value)


class TestGetAll:
    def test_empty_len_eq_zero(self, empty_user_repository):
        assert len(empty_user_repository.get_all()) == 0

    def test_two_user_len_eq_two(self, two_user_repository):
        assert len(two_user_repository.get_all()) == 2


class TestUpdate:
    def test_invalid_id_error(self, user_repository, user_updated_invalid_id):
        with pytest.raises(NotFoundRepoError):
            user_repository.update(user_updated_invalid_id)

    def test_update_name_ok(self, user_repository, user_updated_name, user):
        res = user_repository.update(user_updated_name)

        assert res.name != user.name and res.name == user_updated_name.name


class TestGetByEmail:
    def test_ok(self, user_repository, user):
        found = user_repository.get_by_email(user.email.value)

        assert found == user

    def test_notfound_error(self, empty_user_repository, userschema):
        with pytest.raises(NotFoundRepoError):
            empty_user_repository.get_by_email(userschema.email.value)
