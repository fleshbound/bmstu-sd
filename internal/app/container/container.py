from dependency_injector import containers, providers

from repository.sqlalchemy.animal import SqlAlchemyAnimalRepository
from core.animal.service.impl.animal import AnimalService
from repository.sqlalchemy.breed import SqlAlchemyBreedRepository
from core.breed.service.impl.breed import BreedService
from repository.sqlalchemy.group import SqlAlchemyGroupRepository
from core.group.service.impl.group import GroupService
from repository.sqlalchemy.species import SqlAlchemySpeciesRepository
from core.species.service.impl.species import SpeciesService
from repository.sqlalchemy.user import SqlAlchemyUserRepository
from core.user.service.impl.user import UserService
from repository.sqlalchemy.database.database import SqlAlchemyDatabase
from internal.app.config.config import configs


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "core.animal.api.router.animal",
            "core.user.api.router.user",
            "core.group.api.router.group",
            "core.species.api.router.species",
            "core.breed.api.router.breed",
        ]
    )

    db = providers.Singleton(SqlAlchemyDatabase, db_url=configs.DATABASE_URL)

    animal_repo = providers.Factory(SqlAlchemyAnimalRepository, session_factory=db.provided.session)
    animal_service = providers.Factory(AnimalService, animal_repo=animal_repo)

    user_repo = providers.Factory(SqlAlchemyUserRepository, session_factory=db.provided.session)
    user_service = providers.Factory(UserService, user_repo=user_repo)

    breed_repo = providers.Factory(SqlAlchemyBreedRepository, session_factory=db.provided.session)
    breed_service = providers.Factory(BreedService, breed_repo=breed_repo)

    species_repo = providers.Factory(SqlAlchemySpeciesRepository, session_factory=db.provided.session)
    species_service = providers.Factory(SpeciesService, species_repo=species_repo)

    group_repo = providers.Factory(SqlAlchemyGroupRepository, session_factory=db.provided.session)
    group_service = providers.Factory(GroupService, group_repo=group_repo)
