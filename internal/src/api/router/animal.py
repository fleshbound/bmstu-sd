from typing import List, Union

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from fastapi.responses import PlainTextResponse
from pydantic import PositiveInt, NonNegativeInt

from container.container import Container
from core.animal.schema.animal import AnimalSchemaCreate, AnimalSchema, AnimalSchemaDelete
from core.animal.service.animal import IAnimalService
from core.utils.exceptions import NotFoundRepoError
from core.utils.types import ID

router = APIRouter(
    prefix="/animal",
    tags=["Animal"]
)

dep_animal = Depends(Provide[Container.animal_service])


@router.post("", status_code=status.HTTP_201_CREATED)
@inject
async def create_animal(
        animal_create: AnimalSchemaCreate,
        animal_service: IAnimalService = dep_animal
) -> AnimalSchema:
    new_animal = animal_service.create(animal_create)
    return new_animal


@router.get("")
@inject
async def get_animals(
        skip: NonNegativeInt,
        limit: PositiveInt,
        animal_service: IAnimalService = dep_animal
) -> List[AnimalSchema]:
    return animal_service.get_all(skip, limit)


# @router.get("/{animal_id}")
# @inject
# async def get_animal_by_id(
#         animal_id: PositiveInt,
#         animal_service: IAnimalService = dep_animal
# ) -> AnimalSchema:
#     return animal_service.get_by_id(ID(animal_id))
#

@router.get("/user/{user_id}")
@inject
async def get_animal_by_user(
        user_id: PositiveInt,
        animal_service: IAnimalService = dep_animal
) -> List[AnimalSchema]:
    try:
        res = animal_service.get_by_user_id(ID(user_id))
    except NotFoundRepoError:
        return []
    return res


# @router.delete("/{animal_id}")
# @inject
# async def delete_animal(
#         animal_id: PositiveInt,
#         animal_service: IAnimalService = dep_animal
# ) -> AnimalSchemaDelete:
#     return animal_service.delete(ID(animal_id))
#
#
# @router.post("/{animal_id}")
# @inject
# async def update_animal(
#         animal_update: AnimalSchemaUpdate,
#         animal_service: IAnimalService = dep_animal
# ) -> AnimalSchema:
#     return animal_service.update(animal_update)

@router.delete("/{animal_id}")
@inject
async def delete_animal(
    animal_id: PositiveInt,
    animal_service: IAnimalService = dep_animal
) -> AnimalSchemaDelete:
    try:
        res = animal_service.delete(ID(animal_id))
    except NotFoundRepoError as e:
        return PlainTextResponse(str(e), status_code=404)
    return res


@router.get("/{animal_id}")
@inject
async def get_animal_by_id(
    animal_id: PositiveInt,
    animal_service: IAnimalService = dep_animal
) -> AnimalSchema:
    try:
        res = animal_service.get_by_id(ID(animal_id))
    except NotFoundRepoError as e:
        return PlainTextResponse(str(e), status_code=404)
    return res
