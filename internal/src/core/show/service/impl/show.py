from typing import List

from pydantic import NonNegativeInt, PositiveInt

from internal.src.core.animal.service.animal import IAnimalService
from internal.src.core.breed.service.breed import IBreedService
from internal.src.core.certificate.schema.certificate import CertificateSchemaCreate
from internal.src.core.certificate.service.certificate import ICertificateService
from internal.src.core.show.repository.show import IShowRepository
from internal.src.core.show.schema.animalshow import AnimalShowSchemaCreate
from internal.src.core.show.schema.show import ShowSchemaCreate, ShowSchema, ShowSchemaUpdate, ShowSchemaDetailed, \
    ShowRegisterAnimalResult, ShowSchemaReport, ShowStatus, ShowRegisterAnimalStatus, ShowRegisterUserResult, \
    ShowRegisterUserStatus
from internal.src.core.show.schema.usershow import UserShowSchemaCreate
from internal.src.core.show.service.animalshow import IAnimalShowService
from internal.src.core.show.service.score import IScoreService
from internal.src.core.show.service.show import IShowService
from internal.src.core.show.service.usershow import IUserShowService
from internal.src.core.standard.service.standard import IStandardService
from internal.src.core.user.schema.user import UserRole
from internal.src.core.user.service.user import IUserService
from internal.src.core.utils.exceptions import ShowServiceError, NotFoundRepoError, AnimalShowServiceError, UserShowServiceError
from internal.src.core.utils.types import ID


class ShowService(IShowService):
    show_repo: IShowRepository
    score_service: IScoreService
    animalshow_service: IAnimalShowService
    usershow_service: IUserShowService
    certificate_service: ICertificateService
    animal_service: IAnimalService
    user_service: IUserService
    breed_service: IBreedService
    standard_service: IStandardService

    def __init__(self,
                 show_repo: IShowRepository,
                 score_service: IScoreService,
                 animalshow_service: IAnimalShowService,
                 usershow_service: IUserShowService,
                 certificate_service: ICertificateService,
                 animal_service: IAnimalService,
                 user_service: IUserService,
                 breed_service: IBreedService,
                 standard_service: IStandardService):
        self.show_repo = show_repo
        self.score_service = score_service
        self.animalshow_service = animalshow_service
        self.usershow_service = usershow_service
        self.certificate_service = certificate_service
        self.animal_service = animal_service
        self.user_service = user_service
        self.breed_service = breed_service
        self.standard_service = standard_service

    def create(self, show_create: ShowSchemaCreate) -> ShowSchema:
        new_show = ShowSchema.from_create(show_create)
        if new_show.is_multi_breed:
            if not new_show.breed_id is None:
                raise ShowServiceError(detail=f"multi_breed breed_id not None (create): id={new_show.id},"
                                              f" breed_id={new_show.breed_id}")
            if new_show.species_id is None:
                raise ShowServiceError(detail=f"multi_breed species_id None (create): id={new_show.id}")
            if not new_show.standard_id is None:
                raise ShowServiceError(detail=f"multi_breed standard_id not None (create): id={new_show.id},"
                                              f" standard_id={new_show.standard_id}")
        else:
            if not new_show.species_id is None:
                raise ShowServiceError(detail=f"not multi_breed species_id not None (create): id={new_show.id},"
                                              f" breed_id={new_show.species_id}")
            if new_show.breed_id is None:
                raise ShowServiceError(detail=f"not multi_breed breed_id None (create): id={new_show.id}")
            if new_show.standard_id is None:
                raise ShowServiceError(detail=f"not multi_breed standard_id None (create): id={new_show.id}")

        return self.show_repo.create(new_show)

    def get_usershow_count(self, show_id: ID) -> NonNegativeInt:
        try:
            res = self.usershow_service.get_by_show_id(show_id)
        except NotFoundRepoError:
            return 0
        return len(res)
    
    def get_animalshow_count(self, show_id: ID) -> NonNegativeInt:
        try:
            res = self.animalshow_service.get_by_show_id(show_id)
        except NotFoundRepoError:
            return 0
        return len(res)

    def start(self, show_id: ID) -> ShowSchema:
        cur_show = self.show_repo.get_by_id(show_id)
        
        if cur_show.status != ShowStatus.created:
            raise ShowServiceError(detail=f"show cannot be started: id={show_id}, status={cur_show.status}")
        
        user_count = self.get_usershow_count(show_id)
        if user_count == 0:
            raise ShowServiceError(detail=f"show cannot be started: id={show_id}, user_count={user_count}")

        animal_count = self.get_animalshow_count(show_id)
        if animal_count == 0:
            raise ShowServiceError(detail=f"show cannot be started: id={show_id}, user_count={user_count}")

        cur_show.status = ShowStatus.started
        return self.show_repo.update(cur_show)

    def abort(self, show_id: ID) -> ShowSchema:
        cur_show = self.show_repo.get_by_id(show_id)
        if cur_show.status != ShowStatus.started:
            raise ShowServiceError(detail=f"show cannot be stopped: id={show_id}, status={cur_show.status}")
        cur_show.status = ShowStatus.aborted

        animalshow_records = self.animalshow_service.get_by_show_id(show_id)
        for record in animalshow_records:
            self.animalshow_service.archive(record.id)
        usershow_records = self.usershow_service.get_by_show_id(show_id)
        for record in usershow_records:
            self.usershow_service.archive(record.id)

        return self.show_repo.update(cur_show)

    def stop(self, show_id: ID) -> ShowSchemaReport:
        cur_show = self.show_repo.get_by_id(show_id)
        if cur_show.status != ShowStatus.started:
            raise ShowServiceError(detail=f"show cannot be stopped: id={show_id}, status={cur_show.status}")
        if not self.score_service.all_users_scored(show_id):
            users_scored = self.score_service.get_users_scored_count(show_id)
            raise ShowServiceError(detail=f"show cannot be stopped: id={show_id}, count_scored={users_scored}")
        cur_show.status = ShowStatus.stopped
        self.show_repo.update(cur_show)

        rank_count, ranking_info = self.score_service.get_show_ranking_info(show_id)
        for record in ranking_info:
            cert = CertificateSchemaCreate(
                animalshow_id=record.total_info.record_id,
                rank=record.rank
            )
            self.certificate_service.create(cert)
            self.animalshow_service.archive(record.total_info.record_id)

        usershow_records = self.usershow_service.get_by_show_id(show_id)
        for record in usershow_records:
            self.usershow_service.archive(record.id)

        return ShowSchemaReport(
            ranking_info=ranking_info,
            rank_count=rank_count
        )

    def update(self, show_update: ShowSchemaUpdate) -> ShowSchema:
        show_id = show_update.id
        cur_show = self.show_repo.get_by_id(show_id)
        if cur_show.status != ShowStatus.started:
            raise ShowServiceError(detail=f"show cannot be updated: id={show_id}, status={cur_show.status}")
        new_show = cur_show.from_update(show_update)
        return self.show_repo.update(new_show)

    def get_all(self, skip: NonNegativeInt = 0, limit: PositiveInt = 100) -> List[ShowSchema]:
        return self.show_repo.get_all(skip, limit)

    def get_by_id(self, show_id: ID) -> ShowSchema:
        return self.show_repo.get_by_id(show_id.value)

    def get_by_standard_id(self, standard_id: ID) -> List[ShowSchema]:
        return self.show_repo.get_by_standard_id(standard_id.value)

    def get_by_user_id(self, user_id: ID) -> List[ShowSchema]:
        usershow_records = self.usershow_service.get_by_user_id(user_id)
        res = []
        for record in usershow_records:
            res.append(self.show_repo.get_by_id(record.show_id))
        return res

    def get_by_animal_id(self, animal_id: ID) -> List[ShowSchema]:
        animalshow_records = self.animalshow_service.get_by_animal_id(animal_id)
        res = []
        for record in animalshow_records:
            res.append(self.show_repo.get_by_id(record.show_id))
        return res

    def get_by_id_detailed(self, show_id: ID) -> ShowSchemaDetailed:
        cur_show = self.show_repo.get_by_id(show_id.value)
        animalshow_records = self.animalshow_service.get_by_show_id(show_id)
        animals = []
        for record in animalshow_records:
            animals.append(self.animal_service.get_by_id(record.animal_id))
        usershow_records = self.usershow_service.get_by_show_id(show_id)
        users = []
        for record in usershow_records:
            users.append(self.user_service.get_by_id(record.user_id))
        detailed = ShowSchemaDetailed.from_schema(cur_show)
        detailed.animals = animals
        detailed.users = users
        return detailed

    def register_animal(self, animal_id: ID, show_id: ID) -> ShowRegisterAnimalResult:
        cur_show = self.show_repo.get_by_id(show_id)
        if cur_show.status != ShowStatus.created:
            raise ShowServiceError(detail=f"animal cannot be registered: animal_id={animal_id}, "
                                          f"show_id={show_id}, show_status={cur_show.status}")
        cur_animal = self.animal_service.get_by_id(animal_id)

        if cur_show.is_multi_breed:
            if self.breed_service.get_by_id(cur_animal.breed_id).species_id != cur_show.species_id:
                raise ShowServiceError(detail=f'invalid animal species: animal_id={cur_animal.id}, show_id={show_id}')
        else:
            if cur_animal.breed_id != cur_show.breed_id:
                raise ShowServiceError(detail=f'invalid animal breed: animal_id={cur_animal.id}, show_id={show_id}')
            if not self.standard_service.check_animal_by_standard(cur_show.standard_id, cur_animal):
                raise ShowServiceError(detail=f'invalid animal standard check: animal_id={cur_animal.id},'
                                              f' show_id={show_id}')
        try:
            self.animalshow_service.get_by_animal_show_id(animal_id, show_id)
        except NotFoundRepoError:
            animalshow_record_create = AnimalShowSchemaCreate(animal_id=animal_id, show_id=show_id, is_archived=False)
            animalshow_record = self.animalshow_service.create(animalshow_record_create)
        else:
            raise ShowServiceError(detail=f"animal is already registered: "
                                          f"animal_id={animal_id}, show_id={show_id}")
        return ShowRegisterAnimalResult(
            record_id=animalshow_record.id,
            status=ShowRegisterAnimalStatus.register_ok
        )

    def register_user(self, user_id: ID, show_id: ID) -> ShowRegisterUserResult:
        cur_show = self.show_repo.get_by_id(show_id)
        if cur_show.status != ShowStatus.created:
            raise ShowServiceError(detail=f"user cannot be registered: user_id={user_id}, "
                                          f"show_id={show_id}, show_status={cur_show.status}")
        cur_user = self.user_service.get_by_id(user_id)
        if cur_user.role != UserRole.judge:
            raise ShowServiceError(detail=f"user cannot be registered (not judge): id={user_id},"
                                          f" role={cur_user.role}")
        try:
            self.usershow_service.get_by_user_show_id(user_id, show_id)
        except NotFoundRepoError:
            usershow_record_create = UserShowSchemaCreate(user_id=user_id, show_id=show_id, is_archived=False)
            usershow_record = self.usershow_service.create(usershow_record_create)
        else:
            raise ShowServiceError(detail=f"user is already registered: "
                                          f"user_id={user_id}, show_id={show_id}")
        return ShowRegisterUserResult(
            record_id=usershow_record.id,
            status=ShowRegisterUserStatus.register_ok
        )

    def unregister_animal(self, animal_id: ID, show_id: ID) -> ShowRegisterAnimalResult:
        cur_show = self.show_repo.get_by_id(show_id)
        if cur_show.status != ShowStatus.created:
            raise ShowServiceError(detail=f"animal cannot be registered: animal_id={animal_id}, "
                                          f"show_id={show_id}, show_status={cur_show.status}")
        try:
            record = self.animalshow_service.get_by_animal_show_id(animal_id, show_id)
        except NotFoundRepoError:
            raise ShowServiceError(detail=f"animal's not registered: "
                                          f"animal_id={animal_id}, show_id={show_id}")
        except AnimalShowServiceError as e:
            raise e
        self.animalshow_service.delete(record.id)
        return ShowRegisterAnimalResult(record_id=record.id, status=ShowRegisterAnimalStatus.unregister_ok)

    def unregister_user(self, user_id: ID, show_id: ID) -> ShowRegisterUserResult:
        cur_show = self.show_repo.get_by_id(show_id)
        if cur_show.status != ShowStatus.created:
            raise ShowServiceError(detail=f"user cannot be registered: user_id={user_id}, "
                                          f"show_id={show_id}, show_status={cur_show.status}")
        try:
            record = self.usershow_service.get_by_user_show_id(user_id, show_id)
        except NotFoundRepoError:
            raise ShowServiceError(detail=f"user's not registered: "
                                          f"user_id={user_id}, show_id={show_id}")
        except UserShowServiceError as e:
            raise e
        self.usershow_service.delete(record.id)
        return ShowRegisterUserResult(record_id=record.id, status=ShowRegisterUserStatus.unregister_ok)
