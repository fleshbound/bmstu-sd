from typing import List

from internal.src.core.utils.exceptions import NotFoundRepoError
from internal.src.core.show.schema.animalshow import AnimalShowSchemaCreate, AnimalShowSchema, AnimalShowSchemaDeleted
from internal.src.core.show.service.animalshow import IAnimalShowService
from internal.src.core.utils.types import ID


class MockedAnimalShowService(IAnimalShowService):
    _animalshows: List[AnimalShowSchema]

    def __init__(self, animalshows: List[AnimalShowSchema]):
        self._animalshows = animalshows

    def create(self, animalshow_create: AnimalShowSchemaCreate) -> AnimalShowSchema:
        self._animalshows.append(AnimalShowSchema.from_create(animalshow_create))
        if len(self._animalshows) > 0:
            self._animalshows[-1].id = ID(len(self._animalshows) - 1)
        else:
            self._animalshows[-1].id = ID(0)
        return self._animalshows[-1]

    def archive(self, animalshow_id: ID) -> AnimalShowSchema:
        for record in self._animalshows:
            if record.id == animalshow_id:
                record.is_archived = True
                return record
        raise NotFoundRepoError(detail='')
        # return AnimalShowSchema(
        #     id=animalshow_id,
        #     animal_id=ID(0),
        #     show_id=ID(0),
        #     is_archived=True
        # )

    def delete(self, animalshow_id: ID) -> AnimalShowSchemaDeleted:
        for i, record in enumerate(self._animalshows):
            if record.id == animalshow_id:
                self._animalshows.pop(i)
                return AnimalShowSchemaDeleted(id=animalshow_id)
        return AnimalShowSchemaDeleted(id=animalshow_id)

    def get_by_id(self, id: ID) -> AnimalShowSchema:
        for record in self._animalshows:
            if record.id == id:
                return record
        raise NotFoundRepoError(detail='')
        # return AnimalShowSchema(
        #     id=id,
        #     animal_id=ID(0),
        #     show_id=ID(0),
        #     is_archived=False
        # )

    def get_by_animal_id(self, animal_id: ID) -> List[AnimalShowSchema]:
        res = []
        for record in self._animalshows:
            if record.animal_id == animal_id:
                res.append(record)
        if len(res) == 0:
            raise NotFoundRepoError(detail='')
        return res
        # return [AnimalShowSchema(
        #     id=ID(0),
        #     animal_id=animal_id,
        #     show_id=ID(0),
        #     is_archived=False
        # )]

    def get_by_show_id(self, show_id: ID) -> List[AnimalShowSchema]:
        res = []
        for record in self._animalshows:
            if record.show_id == show_id:
                res.append(record)
        if len(res) == 0:
            raise NotFoundRepoError(detail='')
        return res
        # return [AnimalShowSchema(
        #     id=ID(0),
        #     animal_id=ID(0),
        #     show_id=show_id,
        #     is_archived=False
        # )]

    def get_by_animal_show_id(self, animal_id: ID, show_id: ID) -> AnimalShowSchema:
        for record in self._animalshows:
            if record.show_id == show_id and record.animal_id == animal_id:
                return record
        raise NotFoundRepoError(detail='')
        # return AnimalShowSchema(
        #     id=ID(0),
        #     animal_id=animal_id,
        #     show_id=show_id,
        #     is_archived=False
        # )
    