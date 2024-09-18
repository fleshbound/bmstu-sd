import pytest

from core.show.schema.score import ScoreSchema
from core.utils.types import ID
from internal.tests.builders.schema.score import ScoreSchemaBuilder


@pytest.fixture
def score_repository(container):
    return container.score_repo()


@pytest.fixture
def scoreschema(usershow, animalshow) -> ScoreSchema:
    return (
        ScoreSchemaBuilder()
        .with_test_values()
        .with_usershow_id(usershow.id.value)
        .with_animalshow_id(animalshow.id.value)
        .build()
    )


@pytest.fixture
def score(score_repository, scoreschema) -> ScoreSchema:
    res_score = score_repository.create(scoreschema)
    yield res_score
    score_repository.delete(res_score.id.value)


@pytest.fixture
def created_score(score_repository, scoreschema) -> ScoreSchema:
    res_score = score_repository.create(scoreschema)
    return res_score


@pytest.fixture
def invalid_score_id(score_repository, created_score) -> ID:
    score_repository.delete(created_score.id.value)
    return created_score.id
