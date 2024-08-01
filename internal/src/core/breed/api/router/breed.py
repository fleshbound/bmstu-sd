from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from pydantic import NonNegativeInt, PositiveInt

from core.breed.schema.breed import BreedSchemaCreate, BreedSchema, BreedSchemaUpdate, BreedSchemaUpdateBody
from core.breed.service.breed import IBreedService
from container import Container
from utils.types import ID

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
        breed_id: NonNegativeInt,
        breed_update_body: BreedSchemaUpdateBody,
        breed_service: IBreedService = dep_breed
) -> BreedSchema:
    breed_update = BreedSchemaUpdate(**breed_update_body.dict())
    breed_update.id = ID(breed_id)
    return breed_service.update(breed_update)
