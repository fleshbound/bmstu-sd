from typing import List, Union

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status, APIRouter
from fastapi.responses import PlainTextResponse
from pydantic import NonNegativeInt, PositiveInt

from container.container import Container
from core.auth.schema.auth import AuthDetails, AuthSchemaSignIn
from core.auth.service.auth import IAuthService
from core.utils.exceptions import AuthServiceError
from core.utils.types import ID, Token

router = APIRouter(
    prefix="/auth/jwt",
    tags=["Auth"]
)

dep_auth = Depends(Provide[Container.auth_service])


@router.post("/login")
@inject
def login(
        auth_details: AuthSchemaSignIn,
        auth_service: IAuthService = dep_auth
) -> AuthDetails:
    try:
        res = auth_service.signin(auth_details)
    except AuthServiceError as e:
        return PlainTextResponse(str(e))
    return res


@router.post("/logout")
@inject
def logout(
        token: str,
        auth_service: IAuthService = dep_auth
) -> PlainTextResponse:
    auth_service.logout(Token(value=token))
    return PlainTextResponse('session deleted')
