from dependency_injector import containers, providers

from database import SqlAlchemyDatabase
from repository.sqlalchemy.animal import SqlAlchemyAnimalRepository
from repository.sqlalchemy.animalshow import SqlAlchemyAnimalShowRepository
from repository.sqlalchemy.breed import SqlAlchemyBreedRepository
from repository.sqlalchemy.certificate import SqlAlchemyCertificateRepository
from repository.sqlalchemy.group import SqlAlchemyGroupRepository
from repository.sqlalchemy.score import SqlAlchemyScoreRepository
from repository.sqlalchemy.show import SqlAlchemyShowRepository
from repository.sqlalchemy.species import SqlAlchemySpeciesRepository
from repository.sqlalchemy.standard import SqlAlchemyStandardRepository
from repository.sqlalchemy.user import SqlAlchemyUserRepository
from repository.sqlalchemy.usershow import SqlAlchemyUserShowRepository

TEST_DATABASE_URL = f"postgresql://postgres:postgres@localhost:5432/test_postgres"


class RepositoryContainer(containers.DeclarativeContainer):
    db = providers.Singleton(SqlAlchemyDatabase, db_url=TEST_DATABASE_URL, echo=False)

    animal_repo = providers.Factory(SqlAlchemyAnimalRepository, session_factory=db.provided.session)
    user_repo = providers.Factory(SqlAlchemyUserRepository, session_factory=db.provided.session)
    breed_repo = providers.Factory(SqlAlchemyBreedRepository, session_factory=db.provided.session)
    species_repo = providers.Factory(SqlAlchemySpeciesRepository, session_factory=db.provided.session)
    group_repo = providers.Factory(SqlAlchemyGroupRepository, session_factory=db.provided.session)
    show_repo = providers.Factory(SqlAlchemyShowRepository, session_factory=db.provided.session)
    animalshow_repo = providers.Factory(SqlAlchemyAnimalShowRepository, session_factory=db.provided.session)
    usershow_repo = providers.Factory(SqlAlchemyUserShowRepository, session_factory=db.provided.session)
    score_repo = providers.Factory(SqlAlchemyScoreRepository, session_factory=db.provided.session)
    standard_repo = providers.Factory(SqlAlchemyStandardRepository, session_factory=db.provided.session)
    certificate_repo = providers.Factory(SqlAlchemyCertificateRepository, session_factory=db.provided.session)
