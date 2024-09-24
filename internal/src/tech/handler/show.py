from tech.dto.animal import AnimalDTO
from tech.dto.score import ScoreDTO
from tech.dto.show import ShowDTO
from tech.handler.input import InputHandler
from tech.utils.exceptions import InputException
from tech.utils.lang.langmodel import LanguageModel
from core.show.schema.show import ShowSchemaReport
from core.show.service.animalshow import IAnimalShowService
from core.show.service.score import IScoreService
from core.show.service.show import IShowService
from core.show.service.usershow import IUserShowService
from core.utils.exceptions import NotFoundRepoError, StartShowStatusError, StartShowZeroRecordsError, \
    StopShowStatusError, StopNotAllUsersScoredError, ShowServiceError, UserShowServiceError
from core.utils.types import ID


class ShowHandler:
    lm: LanguageModel
    show_service: IShowService
    usershow_service: IUserShowService
    score_service: IScoreService
    input_handler: InputHandler
    animalshow_service: IAnimalShowService

    def __init__(self,
                 show_service: IShowService,
                 usershow_service: IUserShowService,
                 score_service: IScoreService,
                 input_handler: InputHandler,
                 animalshow_service: IAnimalShowService):
        self.show_service = show_service
        self.usershow_service = usershow_service
        self.score_service = score_service
        self.input_handler = input_handler
        self.animalshow_service = animalshow_service
        self.lm = input_handler.lang_model

    def score_animal(self, user_id: int):
        show_id = self.input_handler.wait_positive_int(self.lm.question_show_id, self.lm.out_question_show_id)
        if show_id is None:
            return
        try:
            record = self.usershow_service.get_by_user_show_id(ID(user_id), ID(show_id))
        except UserShowServiceError as e:
            print(e)
            return
        try:
            dto = ScoreDTO().input_create(record.id.value)
        except InputException as e:
            print(e)
            return
        self.score_service.create(dto.to_schema_create())
        print(self.lm.score_create_success)

    def create_show(self):
        try:
            dto: ShowDTO = ShowDTO().input_create()
        except InputException as e:
            print(e)
            return
        created = self.show_service.create(dto.to_schema_create())
        ShowDTO.from_schema(created).print()
        # todo: try except integrity error (wrong fk)

    def start_show(self):
        show_id = self.input_handler.wait_positive_int(self.lm.question_show_id, self.lm.out_question_show_id)
        if show_id is None:
            return
        try:
            self.show_service.start(ID(show_id))
        except StartShowStatusError:
            print(self.lm.show_start_error_status)
            return
        except StartShowZeroRecordsError as e:
            if e.type == 'user':
                print(self.lm.show_start_error_no_records_user)
            elif e.type == 'animal':
                print(self.lm.show_start_error_no_records_animal)
            return
        print(self.lm.show_start_success)

    def stop_show(self):
        show_id = self.input_handler.wait_positive_int(self.lm.question_show_id, self.lm.out_question_show_id)
        if show_id is None:
            return
        try:
            self.show_service.stop(ID(show_id))
        except StopShowStatusError:
            print(self.lm.show_stop_error_status)
            return
        except StopNotAllUsersScoredError:
            print(self.lm.show_stop_error_not_all_users_scored)
            return
        print(self.lm.show_stop_success)

    def register_animal(self):
        show_id = self.input_handler.wait_positive_int(self.lm.question_show_id, self.lm.out_question_show_id)
        if show_id is None:
            return
        animal_id = self.input_handler.wait_positive_int(self.lm.question_animal_id, self.lm.out_question_animal_id)
        if animal_id is None:
            return
        try:
            self.show_service.register_animal(ID(animal_id), ID(show_id))
        except ShowServiceError as e:
            print(e)
            return
        print(self.lm.register_animal_success)

    def unregister_animal(self):
        show_id = self.input_handler.wait_positive_int(self.lm.question_show_id, self.lm.out_question_show_id)
        if show_id is None:
            return
        animal_id = self.input_handler.wait_positive_int(self.lm.question_animal_id, self.lm.out_question_animal_id)
        if animal_id is None:
            return
        try:
            self.show_service.unregister_animal(ID(animal_id), ID(show_id))
        except ShowServiceError as e:
            print(e)
            return
        print(self.lm.unregister_animal_success)

    def register_user(self):
        show_id = self.input_handler.wait_positive_int(self.lm.question_show_id, self.lm.out_question_show_id)
        if show_id is None:
            return
        user_id = self.input_handler.wait_positive_int(self.lm.question_user_id, self.lm.out_question_user_id)
        if user_id is None:
            return
        try:
            self.show_service.register_user(ID(user_id), ID(show_id))
        except ShowServiceError as e:
            print(e)
            return
        print(self.lm.register_user_success)

    def unregister_user(self):
        show_id = self.input_handler.wait_positive_int(self.lm.question_show_id, self.lm.out_question_show_id)
        if show_id is None:
            return
        user_id = self.input_handler.wait_positive_int(self.lm.question_user_id, self.lm.out_question_user_id)
        if user_id is None:
            return
        try:
            self.show_service.unregister_user(ID(user_id), ID(show_id))
        except ShowServiceError as e:
            print(e)
            return
        print(self.lm.unregister_user_success)

    def get_shows_all(self):
        res = self.show_service.get_all()
        if len(res) == 0:
            print(self.lm.get_empty_result)
            return
        for show in res:
            ShowDTO.from_schema(show).print()

    def get_show_result(self):
        show_id = self.input_handler.wait_positive_int(self.lm.question_show_id, self.lm.out_question_show_id)
        if show_id is None:
            return
        try:
            res: ShowSchemaReport = self.show_service.get_result_by_id(ID(show_id))
        except ShowServiceError as e:
            print(e)
            return
        print(f'{self.lm.out_rank}: {self.lm.out_animal_id}')
        for rank_info in res.ranking_info:
            cur_animal_id = self.animalshow_service.get_by_id(rank_info.total_info.record_id).animal_id.value
            print(f'{self.lm.out_rank} {rank_info.rank}: {cur_animal_id}')

    def get_animals_by_show(self):
        show_id = self.input_handler.wait_positive_int(self.lm.question_show_id, self.lm.out_question_show_id)
        if show_id is None:
            return
        try:
            res = self.show_service.get_by_id_detailed(ID(show_id))
        except NotFoundRepoError:
            print(self.lm.get_empty_result)
            return
        if len(res.animals) == 0:
            print(self.lm.get_empty_result)
            return
        for animal in res.animals:
            AnimalDTO.from_schema(animal).print()
    