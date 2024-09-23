from typing import List

from pydantic import NonNegativeInt, PositiveInt

from core.animal.schema.animal import AnimalSchema
from core.animal.service.animal import IAnimalService
from core.breed.service.breed import IBreedService
from core.certificate.schema.certificate import CertificateSchemaCreate
from core.certificate.service.certificate import ICertificateService
from core.show.repository.show import IShowRepository
from core.show.schema.animalshow import AnimalShowSchemaCreate
from core.show.schema.show import ShowSchemaCreate, ShowSchema, ShowSchemaUpdate, ShowSchemaDetailed, \
    ShowRegisterAnimalResult, ShowSchemaReport, ShowStatus, ShowRegisterAnimalStatus, ShowRegisterUserResult, \
    ShowRegisterUserStatus
from core.show.schema.usershow import UserShowSchemaCreate
from core.show.service.animalshow import IAnimalShowService
from core.show.service.score import IScoreService
from core.show.service.show import IShowService
from core.show.service.usershow import IUserShowService
from core.standard.service.standard import IStandardService
from core.user.schema.user import UserRole
from core.user.service.user import IUserService
from core.utils.exceptions import NotFoundRepoError, \
    RegisterAnimalCheckError, RegisterShowStatusError, RegisterAnimalRegisteredError, \
    RegisterUserRoleError, RegisterUserRegisteredError, UnregisterShowStatusError, UnregisterAnimalNotRegisteredError, \
    UnregisterUserNotRegisteredError, StartShowStatusError, \
    StartShowZeroRecordsError, AbortShowStatusError, StopShowStatusError, StopNotAllUsersScoredError, \
    UpdateShowStatusError, CheckAnimalStandardError, ShowServiceError
from core.utils.types import ID


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
        if not new_show.is_multi_breed:
            if self.standard_service.get_by_id(new_show.standard_id).breed_id != new_show.breed_id:
                raise ShowServiceError('standard breed_id not equal show breed_id')
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
        cur_show = self.show_repo.get_by_id(show_id.value)
        if cur_show.status != ShowStatus.created:
            raise StartShowStatusError(show_id=show_id, show_status=cur_show.status)

        if not self.get_usershow_count(show_id):
            raise StartShowZeroRecordsError(show_id=show_id, type='user')

        if not self.get_animalshow_count(show_id):
            raise StartShowZeroRecordsError(show_id=show_id, type='animal')

        cur_show.status = ShowStatus.started
        return self.show_repo.update(cur_show)

    def abort(self, show_id: ID) -> ShowSchema:
        cur_show = self.show_repo.get_by_id(show_id.value)
        if cur_show.status != ShowStatus.started:
            raise AbortShowStatusError(show_id=show_id, show_status=cur_show.status)
        cur_show.status = ShowStatus.aborted

        self.archive_animals(show_id)
        self.archive_users(show_id)

        return self.show_repo.update(cur_show)

    def stop(self, show_id: ID) -> ShowSchemaReport:
        cur_show = self.show_repo.get_by_id(show_id.value)

        if cur_show.status != ShowStatus.started:
            raise StopShowStatusError(show_id=show_id, show_status=cur_show.status)

        if not self.score_service.all_users_scored(show_id):
            raise StopNotAllUsersScoredError(show_id=show_id, count=self.score_service.get_users_scored_count(show_id))

        cur_show.status = ShowStatus.stopped
        self.show_repo.update(cur_show)

        rank_count, ranking_info = self.score_service.get_show_ranking_info(show_id)
        report = ShowSchemaReport(ranking_info=ranking_info, rank_count=rank_count)
        for record in report.ranking_info:
            cert = CertificateSchemaCreate(animalshow_id=record.total_info.record_id, rank=record.rank)
            self.certificate_service.create(cert)
            self.animalshow_service.archive(record.total_info.record_id)

        self.archive_users(show_id)

        return report

    def get_result_by_id(self, show_id: ID) -> ShowSchemaReport:
        cur_show = self.show_repo.get_by_id(show_id.value)

        if cur_show.status != ShowStatus.stopped:
            raise StopShowStatusError(show_id=show_id, show_status=cur_show.status)

        rank_count, ranking_info = self.score_service.get_show_ranking_info(show_id)
        return ShowSchemaReport(ranking_info=ranking_info, rank_count=rank_count)

    def archive_users(self, show_id: ID):
        usershow_records = self.usershow_service.get_by_show_id(show_id)
        for record in usershow_records:
            self.usershow_service.archive(record.id)

    def archive_animals(self, show_id: ID):
        animalshow_records = self.animalshow_service.get_by_show_id(show_id)
        for record in animalshow_records:
            self.animalshow_service.archive(record.id)

    def update(self, show_update: ShowSchemaUpdate) -> ShowSchema:
        show_id = show_update.id
        cur_show = self.show_repo.get_by_id(show_id.value)
        if cur_show.status != ShowStatus.started:
            raise UpdateShowStatusError(show_id=show_id, show_status=cur_show.status)
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
            res.append(self.show_repo.get_by_id(record.show_id.value))
        return res

    def get_by_animal_id(self, animal_id: ID) -> List[ShowSchema]:
        animalshow_records = self.animalshow_service.get_by_animal_id(animal_id)
        res = []
        for record in animalshow_records:
            res.append(self.show_repo.get_by_id(record.show_id.value))
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

    def check_animal_meets_show_requirements(self, show: ShowSchema, animal: AnimalSchema) -> None:
        if show.is_multi_breed:
            if self.breed_service.get_by_id(animal.breed_id).species_id != show.species_id:
                raise RegisterAnimalCheckError(detail=f'improper animal species', show_id=show.id, animal_id=animal.id)
        else:
            if animal.breed_id != show.breed_id:
                raise RegisterAnimalCheckError(detail=f'improper animal breed', show_id=show.id, animal_id=animal.id)
            try:
                self.standard_service.check_animal_by_standard(show.standard_id, animal)
            except CheckAnimalStandardError:
                raise RegisterAnimalCheckError(detail=f'animal doesn\'t meet the show standard',
                                               animal_id=animal.id, show_id=show.id)

    def is_animal_registered(self, animal_id: ID, show_id: ID) -> bool:
        try:
            self.animalshow_service.get_by_animal_show_id(animal_id, show_id)
        except NotFoundRepoError:
            return False
        return True

    def register_animal(self, animal_id: ID, show_id: ID) -> ShowRegisterAnimalResult:
        cur_show = self.show_repo.get_by_id(show_id.value)
        if cur_show.status != ShowStatus.created:
            raise RegisterShowStatusError(show_id=show_id, show_status=cur_show.status)

        cur_animal = self.animal_service.get_by_id(animal_id)
        self.check_animal_meets_show_requirements(cur_show, cur_animal)

        if self.is_animal_registered(animal_id, show_id):
            raise RegisterAnimalRegisteredError(animal_id=animal_id, show_id=show_id)

        animalshow_record = self.animalshow_service.create(AnimalShowSchemaCreate(animal_id=animal_id, show_id=show_id))
        return ShowRegisterAnimalResult(record_id=animalshow_record.id, status=ShowRegisterAnimalStatus.register_ok)

    def is_user_registered(self, user_id: ID, show_id: ID) -> bool:
        try:
            self.usershow_service.get_by_user_show_id(user_id, show_id)
        except NotFoundRepoError:
            return False
        return True

    def register_user(self, user_id: ID, show_id: ID) -> ShowRegisterUserResult:
        cur_show = self.show_repo.get_by_id(show_id.value)
        if cur_show.status != ShowStatus.created:
            raise RegisterShowStatusError(show_id=show_id, show_status=cur_show.status)

        cur_user = self.user_service.get_by_id(user_id)
        if cur_user.role != UserRole.judge:
            raise RegisterUserRoleError(show_id=show_id, user_id=user_id, role=cur_user.role)

        if self.is_user_registered(user_id, show_id):
            raise RegisterUserRegisteredError(user_id=user_id, show_id=show_id)

        usershow_record = self.usershow_service.create(UserShowSchemaCreate(user_id=user_id, show_id=show_id))
        return ShowRegisterUserResult(record_id=usershow_record.id, status=ShowRegisterUserStatus.register_ok)

    def unregister_animal(self, animal_id: ID, show_id: ID) -> ShowRegisterAnimalResult:
        cur_show = self.show_repo.get_by_id(show_id.value)
        if cur_show.status != ShowStatus.created:
            raise UnregisterShowStatusError(show_id=show_id, show_status=cur_show.status)

        if not self.is_animal_registered(animal_id, show_id):
            raise UnregisterAnimalNotRegisteredError(animal_id=animal_id, show_id=show_id)

        res = self.animalshow_service.delete(self.animalshow_service.get_by_animal_show_id(animal_id, show_id).id)
        return ShowRegisterAnimalResult(record_id=res.id, status=ShowRegisterAnimalStatus.unregister_ok)

    def unregister_user(self, user_id: ID, show_id: ID) -> ShowRegisterUserResult:
        cur_show = self.show_repo.get_by_id(show_id.value)
        if cur_show.status != ShowStatus.created:
            raise UnregisterShowStatusError(show_id=show_id, show_status=cur_show.status)

        if not self.is_user_registered(user_id, show_id):
            raise UnregisterUserNotRegisteredError(user_id=user_id, show_id=show_id)

        res = self.usershow_service.delete(self.usershow_service.get_by_user_show_id(user_id, show_id).id)
        return ShowRegisterUserResult(record_id=res.id, status=ShowRegisterUserStatus.unregister_ok)
