from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from internal.app.container.container import Container
from pydantic import NonNegativeInt, PositiveInt

<<<<<<<< HEAD:internal/src/api/router/breed.py
from internal.src.core.breed.schema.breed import BreedSchemaCreate, BreedSchema, BreedSchemaUpdate
from internal.src.core.breed.service.breed import IBreedService
from internal.src.core.utils.types import ID
|||||||| parent of a759adf (add console UI files):internal/app/src/api/router/breed.py
from internal.app.container.container import Container
from core.breed.schema.breed import BreedSchemaCreate, BreedSchema, BreedSchemaUpdate
from core.breed.service.breed import IBreedService
from core.utils.types import ID
========
from internal.petowo.container.container import Container
from core.breed.schema.breed import BreedSchemaCreate, BreedSchema, BreedSchemaUpdate
from core.breed.service.breed import IBreedService
from core.utils.types import ID
>>>>>>>> a759adf (add console UI files):internal/petowo/src/api/router/breed.py

router = APIRouter(
    prefix="/breed",
    tags=["Breed"]
)

dep_breed = Depends(Provide[Container.breed_service])


@router.post("", status_code=status.HTTP_201_CREATED)
@inject
async def create_breed(
        breed_create: BreedSchemaCreate,
        breed_service: IBreedService = dep_breed
) -> BreedSchema:
    new_breed = breed_service.create(breed_create)
    return new_breed


@router.get("/all")
@inject
async def get_breed_all(
        skip: NonNegativeInt,
        limit: PositiveInt,
        breed_service: IBreedService = dep_breed
) -> List[BreedSchema]:
    return breed_service.get_all(skip, limit)


@router.get("/{breed_id}")
@inject
async def get_breed_by_id(
        breed_id: NonNegativeInt,
        breed_service: IBreedService = dep_breed
) -> BreedSchema:
    return breed_service.get_by_id(ID(breed_id))


@router.get("/species/{species_id}")
@inject
async def get_breed_by_species_id(
        species_id: NonNegativeInt,
        breed_service: IBreedService = dep_breed
) -> List[BreedSchema]:
    return breed_service.get_by_species_id(ID(species_id))


@router.delete("/{breed_id}")
@inject
async def delete_breed(
        breed_id: NonNegativeInt,
        breed_service: IBreedService = dep_breed
) -> BreedSchema:
    return breed_service.delete(ID(breed_id))


@router.post("/{breed_id}")
@inject
async def update_breed(
        breed_update: BreedSchemaUpdate,
        breed_service: IBreedService = dep_breed
) -> BreedSchema:
    return breed_service.update(breed_update)
