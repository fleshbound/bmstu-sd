from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from pydantic import NonNegativeInt, PositiveInt

from internal.petowo.container.container import Container
from core.group.schema.group import GroupSchemaCreate, GroupSchema, GroupSchemaUpdate
from core.group.service.group import IGroupService
from core.utils.types import ID

router = APIRouter(
    prefix="/group",
    tags=["Group"]
)

dep_group = Depends(Provide[Container.group_service])


@router.post("", status_code=status.HTTP_201_CREATED)
@inject
async def create_group(
        group_create: GroupSchemaCreate,
        group_service: IGroupService = dep_group
) -> GroupSchema:
    new_group = group_service.create(group_create)
    return new_group


@router.get("/all")
@inject
async def get_group_all(
        skip: NonNegativeInt,
        limit: PositiveInt,
        group_service: IGroupService = dep_group
) -> List[GroupSchema]:
    return group_service.get_all(skip, limit)


@router.get("/{group_id}")
@inject
async def get_group_by_id(
        group_id: NonNegativeInt,
        group_service: IGroupService = dep_group
) -> GroupSchema:
    return group_service.get_by_id(ID(group_id))


@router.get("/group/{group_id}")
@inject
async def get_group_by_group_id(
        group_id: NonNegativeInt,
        group_service: IGroupService = dep_group
) -> List[GroupSchema]:
    return group_service.get_by_group_id(ID(group_id))


@router.delete("/{group_id}")
@inject
async def delete_group(
        group_id: NonNegativeInt,
        group_service: IGroupService = dep_group
) -> GroupSchema:
    return group_service.delete(ID(group_id))


@router.post("/{group_id}")
@inject
async def update_group(
        group_update: GroupSchemaUpdate,
        group_service: IGroupService = dep_group
) -> GroupSchema:
    return group_service.update(group_update)
