from typing import List, Union

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from pydantic import NonNegativeInt, PositiveInt

from container.container import Container
from core.animal.schema.animal import AnimalSchema
from core.show.schema.show import ShowSchema, ShowSchemaReport, \
    ShowRegisterAnimalResult
from core.show.service.show import IShowService
from core.utils.exceptions import NotFoundRepoError, ShowServiceError
from core.utils.types import ID

router = APIRouter(
    prefix="/show",
    tags=["Show"]
)

dep_show = Depends(Provide[Container.show_service])


@router.get("")
@inject
async def get_shows(
        skip: NonNegativeInt,
        limit: PositiveInt,
        show_service: IShowService = dep_show
) -> List[ShowSchema]:
    return show_service.get_all(skip, limit)


@router.get("/{show_id}/results")
@inject
async def get_show_result(
        show_id: PositiveInt,
        show_service: IShowService = dep_show
) -> ShowSchemaReport:
    try:
        res = show_service.get_result_by_id(ID(show_id))
    except NotFoundRepoError as e:
        return PlainTextResponse(str(e), status_code=404)
    return res


@router.get("/{show_id}/animals")
@inject
async def get_show_animals(
        show_id: PositiveInt,
        show_service: IShowService = dep_show
) -> List[AnimalSchema]:
    try:
        res = show_service.get_by_id_detailed(show_id)
    except NotFoundRepoError as e:
        return []
    return res.animals


@router.post("/{show_id}/stop")
@inject
async def stop_show(
        show_id: PositiveInt,
        show_service: IShowService = dep_show
) -> ShowSchemaReport:
    try:
        res = show_service.stop(ID(show_id))
    except NotFoundRepoError as e:
        return PlainTextResponse(str(e), status_code=404)
    return res


@router.post("/{show_id}/start")
@inject
async def start_show(
        show_id: PositiveInt,
        show_service: IShowService = dep_show
) -> ShowSchema:
    try:
        res = show_service.start(ID(show_id))
    except ShowServiceError as e:
        return PlainTextResponse(str(e))
    except NotFoundRepoError as e:
        return PlainTextResponse(str(e), status_code=404)
    return res


@router.post("/{show_id}/animals/{animal_id}/register")
@inject
async def start_show(
        show_id: PositiveInt,
        animal_id: PositiveInt,
        show_service: IShowService = dep_show
) -> ShowRegisterAnimalResult:
    return show_service.register_animal(ID(animal_id), ID(show_id))


@router.post("/{show_id}/animals/{animal_id}/unregister")
@inject
async def start_show(
        show_id: PositiveInt,
        animal_id: PositiveInt,
        show_service: IShowService = dep_show
) -> ShowRegisterAnimalResult:
    return show_service.unregister_animal(ID(animal_id), ID(show_id))


@router.post("/{show_id}/users/{user_id}/register")
@inject
async def start_show(
        show_id: PositiveInt,
        user_id: PositiveInt,
        show_service: IShowService = dep_show
) -> ShowRegisterAnimalResult:
    return show_service.register_user(ID(user_id), ID(show_id))


@router.post("/{show_id}/users/{user_id}/unregister")
@inject
async def start_show(
        show_id: PositiveInt,
        user_id: PositiveInt,
        show_service: IShowService = dep_show
) -> ShowRegisterAnimalResult:
    return show_service.unregister_user(ID(user_id), ID(show_id))
