import pytest

from internal.tests.repository.container.container import RepositoryContainer


@pytest.fixture
def container():
    return RepositoryContainer()
