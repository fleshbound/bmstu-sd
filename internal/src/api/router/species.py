from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from pydantic import NonNegativeInt, PositiveInt

from internal.app.container.container import Container
from core.species.schema.species import SpeciesSchemaCreate, SpeciesSchema, SpeciesSchemaUpdate
from core.species.service.species import ISpeciesService
from core.utils.types import ID

router = APIRouter(
    prefix="/species",
    tags=["Species"]
)

dep_species = Depends(Provide[Container.species_service])


@router.post("", status_code=status.HTTP_201_CREATED)
@inject
async def create_species(
        species_create: SpeciesSchemaCreate,
        species_service: ISpeciesService = dep_species
) -> SpeciesSchema:
    new_species = species_service.create(species_create)
    return new_species


@router.get("/all")
@inject
async def get_species_all(
        skip: NonNegativeInt,
        limit: PositiveInt,
        species_service: ISpeciesService = dep_species
) -> List[SpeciesSchema]:
    return species_service.get_all(skip, limit)


@router.get("/{species_id}")
@inject
async def get_species_by_id(
        species_id: NonNegativeInt,
        species_service: ISpeciesService = dep_species
) -> SpeciesSchema:
    return species_service.get_by_id(ID(species_id))


@router.get("/group/{group_id}")
@inject
async def get_species_by_group_id(
        group_id: NonNegativeInt,
        species_service: ISpeciesService = dep_species
) -> List[SpeciesSchema]:
    return species_service.get_by_group_id(ID(group_id))


@router.delete("/{species_id}")
@inject
async def delete_species(
        species_id: NonNegativeInt,
        species_service: ISpeciesService = dep_species
) -> SpeciesSchema:
    return species_service.delete(ID(species_id))


@router.post("/{species_id}")
@inject
async def update_species(
        species_update: SpeciesSchemaUpdate,
        species_service: ISpeciesService = dep_species
) -> SpeciesSchema:
    return species_service.update(species_update)
