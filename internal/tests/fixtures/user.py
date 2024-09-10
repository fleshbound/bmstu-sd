import pytest

from internal.src.core.user.schema.user import UserSchema
from internal.tests.builders.schema.user import UserSchemaBuilder


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
