from dependency_injector import containers, providers

from internal.src.repository.sqlalchemy.animal import SqlAlchemyAnimalRepository
from internal.src.core.animal.service.impl.animal import AnimalService
from internal.src.repository.sqlalchemy.breed import SqlAlchemyBreedRepository
from internal.src.core.breed.service.impl.breed import BreedService
from internal.src.repository.sqlalchemy.group import SqlAlchemyGroupRepository
from internal.src.core.group.service.impl.group import GroupService
from internal.src.repository.sqlalchemy.species import SqlAlchemySpeciesRepository
from internal.src.core.species.service.impl.species import SpeciesService
from internal.src.repository.sqlalchemy.user import SqlAlchemyUserRepository
from internal.src.core.user.service.impl.user import UserService
from internal.src.database.database import SqlAlchemyDatabase
from internal.src.config.config import configs


class Container(containers.DeclarativeContainer):
    # wiring_config = containers.WiringConfiguration(
    #     modules=[
    #         "internal.src.core.animal.api.router.animal",
    #         "internal.src.core.user.api.router.user",
    #         "internal.src.core.group.api.router.group",
    #         "internal.src.core.species.api.router.species",
    #         "internal.src.core.breed.api.router.breed",
    #     ]
    # )
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
