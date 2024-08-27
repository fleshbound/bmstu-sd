from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from internal.app.container.container import Container
from pydantic import NonNegativeInt, PositiveInt

<<<<<<<< HEAD:internal/src/api/router/animal.py
from internal.src.core.animal.schema.animal import AnimalSchemaCreate, AnimalSchema, AnimalSchemaUpdate
from internal.src.core.animal.service.animal import IAnimalService
from internal.src.core.utils.types import ID
|||||||| parent of a759adf (add console UI files):internal/app/src/api/router/animal.py
from internal.app.container.container import Container
from core.animal.schema.animal import AnimalSchemaCreate, AnimalSchema, AnimalSchemaUpdate
from core.animal.service.animal import IAnimalService
from core.utils.types import ID
========
from internal.petowo.container.container import Container
from core.animal.schema.animal import AnimalSchemaCreate, AnimalSchema, AnimalSchemaUpdate
from core.animal.service.animal import IAnimalService
from core.utils.types import ID
>>>>>>>> a759adf (add console UI files):internal/petowo/src/api/router/animal.py

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


@router.get("/all")
@inject
async def get_animal_all(
        skip: NonNegativeInt,
        limit: PositiveInt,
        animal_service: IAnimalService = dep_animal
) -> List[AnimalSchema]:
    return animal_service.get_all(skip, limit)


@router.get("/{animal_id}")
@inject
async def get_animal_by_id(
        animal_id: NonNegativeInt,
        animal_service: IAnimalService = dep_animal
) -> AnimalSchema:
    return animal_service.get_by_id(ID(animal_id))


@router.get("/user/{user_id}")
@inject
async def get_animal_by_user(
        user_id: NonNegativeInt,
        animal_service: IAnimalService = dep_animal
) -> List[AnimalSchema]:
    return animal_service.get_by_user_id(ID(user_id))


@router.delete("/{animal_id}")
@inject
async def delete_animal(
        animal_id: NonNegativeInt,
        animal_service: IAnimalService = dep_animal
) -> AnimalSchema:
    return animal_service.archive(ID(animal_id))


@router.post("/{animal_id}")
@inject
async def update_animal(
        animal_update: AnimalSchemaUpdate,
        animal_service: IAnimalService = dep_animal
) -> AnimalSchema:
    return animal_service.update(animal_update)
