from typing import List

from pydantic import NonNegativeInt, PositiveInt

from core.animal.service.animal import IAnimalService
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
from core.user.schema.user import UserRole
from core.user.service.user import IUserService
from utils.exceptions import ShowServiceError, NotFoundRepoError
from utils.types import ID


class ShowService(IShowService):
    show_repo: IShowRepository
    score_service: IScoreService
    animalshow_service: IAnimalShowService
    usershow_service: IUserShowService
    certificate_service: ICertificateService
    animal_service: IAnimalService
    user_service: IUserService

    def __init__(self,
                 show_repo: IShowRepository,
                 score_service: IScoreService,
                 animalshow_service: IAnimalShowService,
                 usershow_service: IUserShowService,
                 certificate_service: ICertificateService,
                 animal_service: IAnimalService,
                 user_service: IUserService):
        self.show_repo = show_repo
        self.score_service = score_service
        self.animalshow_service = animalshow_service
        self.usershow_service = usershow_service
        self.certificate_service = certificate_service
        self.animal_service = animal_service

    def create(self, show_create: ShowSchemaCreate) -> ShowSchema:
        raise NotImplementedError
    
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
        if user_count == 0:
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
        cur_show = self.show_repo.get_by_id(show_update.id)
        new_show = cur_show.from_update(show_update)
        return self.show_repo.update(new_show)

    def get_all(self, skip: NonNegativeInt = 0, limit: PositiveInt = 100) -> List[ShowSchema]:
        return self.show_repo.get_all(skip, limit)

    def get_by_id(self, show_id: ID) -> ShowSchema:
        return self.show_repo.get_by_id(show_id)

    def get_by_user_id(self, user_id: ID) -> List[ShowSchema]:
        usershow_records = self.usershow_service.get_by_user_id(user_id)
        res = []
        for record in usershow_records:
            res.append(self.show_repo.get_by_id(record.show_id))
        return res

    def get_by_user_id(self, user_id: ID) -> List[ShowSchema]:
        animalshow_records = self.animalshow_service.get_by_user_id(user_id)
        res = []
        for record in animalshow_records:
            res.append(self.show_repo.get_by_id(record.show_id))
        return res

    def get_by_id_detailed_animals(self) -> ShowSchemaDetailed:
        pass

    def get_by_id_detailed_users(self) -> ShowSchemaDetailed:
        pass

    def register_animal(self, user_id: ID, show_id: ID) -> ShowRegisterAnimalResult:
        cur_show = self.show_repo.get_by_id(show_id)
        if cur_show.status != ShowStatus.created:
            raise ShowServiceError(detail=f"animal cannot be registered: user_id={user_id}, "
                                          f"show_id={show_id}, show_status={cur_show.status}")
        cur_animal = self.animal_service.get_by_id(user_id)
        # todo: check animal species
        # todo: check animal breed
        # todo: check animal by standard if show isn't multi-breed
        try:
            self.animalshow_service.get_by_animal_show_id(user_id, show_id)
        except NotFoundRepoError:
            animalshow_record_create = AnimalShowSchemaCreate(user_id=user_id, show_id=show_id, is_archived=False)
            animalshow_record = self.animalshow_service.create(animalshow_record_create)
        else:
            raise ShowServiceError(detail=f"animal is already registered: "
                                          f"user_id={user_id}, show_id={show_id}")

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
            self.animalshow_service.get_by_animal_show_id(user_id, show_id)
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
