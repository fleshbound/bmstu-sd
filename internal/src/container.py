from dependency_injector import containers, providers

from core.animal.repository.sqlalchemy.animal import SqlAlchemyAnimalRepository
from core.animal.service.impl.animal import AnimalService
from core.user.repository.sqlalchemy.user import SqlAlchemyUserRepository
from core.user.service.impl.user import UserService
from database.database import Database
from config import configs


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "core.animal.api.router.animal",
            "core.user.api.router.user",
        ]
    )

    db = providers.Singleton(Database, db_url=configs.DATABASE_URL)
    animal_repo = providers.Factory(SqlAlchemyAnimalRepository, session_factory=db.provided.session)
    animal_service = providers.Factory(AnimalService, animal_repo=animal_repo)
    user_repo = providers.Factory(SqlAlchemyUserRepository, session_factory=db.provided.session)
    user_service = providers.Factory(UserService, user_repo=user_repo)
