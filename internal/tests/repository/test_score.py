import pytest

from internal.src.core.utils.exceptions import NotFoundRepoError, ValidationRepoError
from internal.src.core.utils.types import ID
from internal.tests.builders.schema.score import ScoreSchemaBuilder


@pytest.fixture
def usershow_id_no_score(score_repository, usershow) -> ID:
    for a in score_repository.get_all():
        score_repository.delete(a.id.value)
    yield usershow.id


@pytest.fixture
def usershow_id_one_score(score_repository, usershow_id_no_score, animalshow):
    res = score_repository.create(
        ScoreSchemaBuilder()
        .with_test_values()
        .with_usershow_id(usershow_id_no_score.value)
        .with_animalshow_id(animalshow.id.value)
        .build()
    )
    return res.usershow_id


@pytest.fixture
def animalshow_id_no_score(score_repository, animalshow) -> ID:
    for a in score_repository.get_all():
        score_repository.delete(a.id.value)
    yield animalshow.id


@pytest.fixture
def animalshow_id_one_score(score_repository, animalshow_id_no_score, usershow):
    res = score_repository.create(
        ScoreSchemaBuilder()
        .with_test_values()
        .with_usershow_id(usershow.id.value)
        .with_animalshow_id(animalshow_id_no_score.value)
        .build()
    )
    return res.animalshow_id


@pytest.fixture
def score_updated_invalid_id(invalid_score_id):
    return (
        ScoreSchemaBuilder()
        .with_test_values()
        .with_id(invalid_score_id.value)
        .build()
    )


@pytest.fixture
def score_updated_is_archived(score):
    return (
        ScoreSchemaBuilder()
        .from_object(score)
        .with_is_archived(True)
        .build()
    )


@pytest.fixture
def score_updated_usershow_id(score, usershow_repository, usershowschema):
    return (
        ScoreSchemaBuilder()
        .from_object(score)
        .with_usershow_id(usershow_repository.create(usershowschema).id.value)
        .build()
    )


@pytest.fixture
def score_updated_animalshow_id(score, animalshow_repository, animalshowschema):
    return (
        ScoreSchemaBuilder()
        .from_object(score)
        .with_animalshow_id(animalshow_repository.create(animalshowschema).id.value)
        .build()
    )


@pytest.fixture
def empty_score_repository(score_repository):
    for a in score_repository.get_all():
        score_repository.delete(a.id.value)
    return score_repository


@pytest.fixture
def two_score_repository(empty_score_repository, scoreschema):
    empty_score_repository.create(scoreschema)
    empty_score_repository.create(scoreschema)
    return empty_score_repository


@pytest.fixture
def score_updated_invalid_usershow_id(score, invalid_usershow_id, animalshow):
    return (
        ScoreSchemaBuilder()
        .from_object(score)
        .with_usershow_id(invalid_usershow_id.value)
        .with_animalshow_id(animalshow.id.value)
        .build()
    )


@pytest.fixture
def score_updated_invalid_animalshow_id(score, invalid_animalshow_id, usershow):
    return (
        ScoreSchemaBuilder()
        .from_object(score)
        .with_animalshow_id(invalid_animalshow_id.value)
        .with_usershow_id(usershow.id.value)
        .build()
    )


class TestCreate:
    def test_ok(self, score_repository, scoreschema):
        created = score_repository.create(scoreschema)

        result = score_repository.get_by_id(created.id.value)
        tmp = scoreschema
        tmp.id = created.id
        assert result == tmp


class TestGetById:
    def test_ok(self, score_repository, score):
        found = score_repository.get_by_id(score.id.value)

        assert found == score

    def test_notfound_error(self, score_repository, invalid_score_id: ID):
        with pytest.raises(NotFoundRepoError):
            score_repository.get_by_id(invalid_score_id.value)


class TestDelete:
    def test_ok(self, score_repository, created_score):
        score_repository.delete(created_score.id.value)

        with pytest.raises(NotFoundRepoError):
            score_repository.get_by_id(created_score.id.value)

    def test_notfound_error(self, score_repository, invalid_score_id: ID):
        with pytest.raises(NotFoundRepoError):
            score_repository.delete(invalid_score_id.value)


class TestGetByUserShowId:
    def test_no_score_error(self, score_repository, usershow_id_no_score):
        with pytest.raises(NotFoundRepoError):
            score_repository.get_by_usershow_id(usershow_id_no_score.value)

    def test_one_score_ok(self, score_repository, usershow_id_one_score):
        res = score_repository.get_by_usershow_id(usershow_id_one_score.value)

        assert len(res) == 1


class TestGetByAnimalShowId:
    def test_no_score_error(self, score_repository, animalshow_id_no_score):
        with pytest.raises(NotFoundRepoError):
            score_repository.get_by_animalshow_id(animalshow_id_no_score.value)

    def test_one_score_ok(self, score_repository, animalshow_id_one_score):
        res = score_repository.get_by_animalshow_id(animalshow_id_one_score.value)

        assert len(res) == 1


class TestGetAll:
    def test_empty_len_eq_zero(self, empty_score_repository):
        assert len(empty_score_repository.get_all()) == 0

    def test_two_score_len_eq_two(self, two_score_repository):
        assert len(two_score_repository.get_all()) == 2


class TestUpdate:
    def test_invalid_id_error(self, score_repository, score_updated_invalid_id):
        with pytest.raises(NotFoundRepoError):
            score_repository.update(score_updated_invalid_id)

    def test_update_is_archived_ok(self, score_repository, score_updated_is_archived, score):
        res = score_repository.update(score_updated_is_archived)

        assert res.is_archived != score.is_archived and res.is_archived == score_updated_is_archived.is_archived

    def test_invalid_usershow_id_error(self, score_repository, score_updated_invalid_usershow_id):
        with pytest.raises(ValidationRepoError):
            score_repository.update(score_updated_invalid_usershow_id)

    def test_usershow_id_ok(self, score_repository, score, score_updated_usershow_id):
        res = score_repository.update(score_updated_usershow_id)

        assert res.usershow_id != score.usershow_id and res.usershow_id == score_updated_usershow_id.usershow_id

    def test_invalid_animalshow_id_error(self, score_repository, score_updated_invalid_animalshow_id):
        with pytest.raises(ValidationRepoError):
            score_repository.update(score_updated_invalid_animalshow_id)

    def test_animalshow_id_ok(self, score_repository, score, score_updated_animalshow_id):
        res = score_repository.update(score_updated_animalshow_id)

        assert (res.animalshow_id != score.animalshow_id and
                res.animalshow_id == score_updated_animalshow_id.animalshow_id)
