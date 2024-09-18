from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status, APIRouter
from pydantic import NonNegativeInt, PositiveInt

from container.container import Container
from core.user.schema.user import UserSchemaCreate, UserSchema, UserSchemaUpdate
from core.user.service.user import IUserService
from core.utils.types import ID

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

dep_user = Depends(Provide[Container.user_service])


@router.post("", status_code=status.HTTP_201_CREATED)
@inject
async def create_user(
        user_create: UserSchemaCreate,
        user_service: IUserService = dep_user
) -> UserSchema:
    new_user = user_service.create(user_create)
    return new_user


@router.get("")
@inject
async def get_user_all(
        skip: NonNegativeInt,
        limit: PositiveInt,
        user_service: IUserService = dep_user
) -> List[UserSchema]:
    return user_service.get_all(skip, limit)


@router.get("/{user_id}")
@inject
async def get_user_by_id(
        user_id: NonNegativeInt,
        user_service: IUserService = dep_user
) -> UserSchema:
    return user_service.get_by_id(ID(user_id))


@router.post("/{user_id}")
@inject
async def update_user(
        user_update: UserSchemaUpdate,
        user_service: IUserService = dep_user
) -> UserSchema:
    return user_service.update(user_update)
