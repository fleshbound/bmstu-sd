from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from pydantic import NonNegativeInt, PositiveInt

from core.animal.schema.animal import AnimalSchemaCreate, AnimalSchema, AnimalSchemaUpdate, AnimalSchemaUpdateBody
from core.animal.service.animal import IAnimalService
from container import Container
from utils.types import ID

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
async def get_animal_by_id(
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
        animal_id: NonNegativeInt,
        animal_update_body: AnimalSchemaUpdateBody,
        animal_service: IAnimalService = dep_animal
) -> AnimalSchema:
    animal_update = AnimalSchemaUpdate(**animal_update_body.dict())
    animal_update.id = ID(animal_id)
    return animal_service.update(animal_update)
