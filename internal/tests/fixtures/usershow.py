import pytest

from internal.src.core.show.schema.usershow import UserShowSchema
from internal.src.core.utils.types import ID
from internal.tests.builders.usershow import UserShowSchemaBuilder


@pytest.fixture
def usershow_repository(container):
    return container.usershow_repo()


@pytest.fixture
def usershowschema(show, user) -> UserShowSchema:
    return (
        UserShowSchemaBuilder()
        .with_test_values()
        .with_show_id(show.id.value)
        .with_user_id(user.id.value)
        .build()
    )


@pytest.fixture
def usershow(usershow_repository, usershowschema) -> UserShowSchema:
    res_usershow = usershow_repository.create(usershowschema)
    yield res_usershow
    usershow_repository.delete(res_usershow.id.value)


@pytest.fixture
def created_usershow(usershow_repository, usershowschema) -> UserShowSchema:
    res_usershow = usershow_repository.create(usershowschema)
    return res_usershow


@pytest.fixture
def invalid_usershow_id(usershow_repository, created_usershow) -> ID:
    usershow_repository.delete(created_usershow.id.value)
    return created_usershow.id
