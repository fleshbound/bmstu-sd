from typing import List

import pytest
from fastapi import HTTPException
from pydantic import NonNegativeInt

from core.mock.provider.auth import MockedAuthProvider
from core.mock.service.user import MockedUserService
from internal.src.core.auth.schema.auth import AuthSchemaSignIn, Fingerprint
from internal.src.core.auth.service.impl.auth import AuthService
from internal.src.core.user.schema.user import UserSchema, UserRole
from internal.src.core.utils.types import UserName, HashedPassword, Email, ID


def auth_service_create(users: List[UserSchema],
                        do_verify: bool,
                        fingerprint_ok: bool):
    return AuthService(user_service=MockedUserService(users),
                       auth_provider=MockedAuthProvider(do_verify=do_verify, fingerprint_ok=fingerprint_ok))


def mocked_userschema(id: NonNegativeInt, email: str, password: str):
    return UserSchema(
            id=ID(id),
            email=Email(email),
            hashed_password=HashedPassword(password),
            role=UserRole.guest,
            name=UserName('Cool Bob')
        )


def mocked_authschemasignin(email: str, fingerprint: str, password: str):
    return AuthSchemaSignIn(email=Email(email), fingerprint=Fingerprint(value=fingerprint), password=password)


def test_signin_notfound_error():
    users = [mocked_userschema(0, 'email@mail.ru', 'coolpassword')]
    auth_service = auth_service_create(users, True, True)
    params = mocked_authschemasignin(email='notthisemail@mail.ru',
                                     fingerprint='fingerprint123',
                                     password='coolpassword')
    with pytest.raises(HTTPException):
        auth_service.signin(params)


def test_signin_wrongpassword_error():
    users = [mocked_userschema(0, 'email@mail.ru', 'coolpassword')]
    auth_service = auth_service_create(users, True, True)
    params = mocked_authschemasignin(email='email@mail.ru',
                                     fingerprint='fingerprint123',
                                     password='wrong')
    with pytest.raises(HTTPException):
        auth_service.signin(params)


def test_signin_ok():
    users = [mocked_userschema(0, 'email@mail.ru', 'coolpassword')]
    auth_service = auth_service_create(users, True, True)
    params = mocked_authschemasignin(email='email@mail.ru',
                                     fingerprint='fingerprint123',
                                     password='coolpassword')
    auth_service.signin(params)
