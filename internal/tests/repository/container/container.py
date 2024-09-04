from dependency_injector import containers, providers

from internal.src.repository.sqlalchemy.animal import SqlAlchemyAnimalRepository
from internal.src.repository.sqlalchemy.breed import SqlAlchemyBreedRepository
from internal.src.repository.sqlalchemy.group import SqlAlchemyGroupRepository
from internal.src.repository.sqlalchemy.species import SqlAlchemySpeciesRepository
from internal.src.repository.sqlalchemy.user import SqlAlchemyUserRepository
from internal.src.database.database import SqlAlchemyDatabase
from internal.database.py.dbconfig import DB_HOST, DB_USER, DB_PWD, DB_PORT, DB_NAME

TEST_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Container(containers.DeclarativeContainer):
    db = providers.Singleton(SqlAlchemyDatabase, db_url=TEST_DATABASE_URL)

    animal_repo = providers.Factory(SqlAlchemyAnimalRepository, session_factory=db.provided.session)
    user_repo = providers.Factory(SqlAlchemyUserRepository, session_factory=db.provided.session)
    breed_repo = providers.Factory(SqlAlchemyBreedRepository, session_factory=db.provided.session)
    species_repo = providers.Factory(SqlAlchemySpeciesRepository, session_factory=db.provided.session)
    group_repo = providers.Factory(SqlAlchemyGroupRepository, session_factory=db.provided.session)
