from dependency_injector import containers, providers

from internal.src.database.database import SqlAlchemyDatabase
from internal.src.repository.sqlalchemy.animal import SqlAlchemyAnimalRepository
from internal.src.repository.sqlalchemy.animalshow import SqlAlchemyAnimalShowRepository
from internal.src.repository.sqlalchemy.breed import SqlAlchemyBreedRepository
from internal.src.repository.sqlalchemy.certificate import SqlAlchemyCertificateRepository
from internal.src.repository.sqlalchemy.group import SqlAlchemyGroupRepository
from internal.src.repository.sqlalchemy.score import SqlAlchemyScoreRepository
from internal.src.repository.sqlalchemy.show import SqlAlchemyShowRepository
from internal.src.repository.sqlalchemy.species import SqlAlchemySpeciesRepository
from internal.src.repository.sqlalchemy.standard import SqlAlchemyStandardRepository
from internal.src.repository.sqlalchemy.user import SqlAlchemyUserRepository
from internal.src.repository.sqlalchemy.usershow import SqlAlchemyUserShowRepository

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
