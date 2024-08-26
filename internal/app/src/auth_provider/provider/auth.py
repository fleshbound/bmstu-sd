import uuid
from datetime import datetime, timedelta, timezone

import jwt
from Cryptodome.Hash import SHA256
from internal.src.auth_provider.storage.auth import ISessionStorage, AuthSession
from pydantic import BaseModel

from internal.src.auth_provider.utils.exceptions import AuthProviderError
from internal.src.core.auth.provider.auth import IAuthProvider
from internal.src.core.auth.schema.auth import Token, Fingerprint, AuthDetails, AuthPayload
from internal.src.core.utils.types import HashedPassword, ID


class AuthConfig(BaseModel):
    secret: str
    access_token_time: timedelta
    refresh_token_time: timedelta


class AuthProvider(IAuthProvider):
    session_storage: ISessionStorage
    config: AuthConfig

    def __init__(self, config: AuthConfig, session_storage: ISessionStorage):
        self.session_storage = session_storage
        self.config = config

    def create_jwt_session(self, payload: AuthPayload, fingerprint: Fingerprint) -> AuthDetails:
        access_expire_time = self.config.access_token_time
        access_expire_dt: datetime = datetime.now(timezone.utc) + access_expire_time
        claims = {"exp": access_expire_dt, "user_id": str(payload.user_id.value)}
        access_token = jwt.encode(payload=claims, key=self.config.secret, algorithm='HS256')

        refresh_token = str(uuid.uuid4())
        refresh_expire_time = self.config.refresh_token_time
        refresh_expire_dt = datetime.now(timezone.utc) + refresh_expire_time
        session = AuthSession(
            refresh_token=Token(value=refresh_token),
            refresh_expire_dt=refresh_expire_dt,
            fingerprint=fingerprint,
            payload=payload
        )

        self.session_storage.put(refresh_token, session, refresh_expire_time)

        return AuthDetails(
            access_token=Token(value=access_token),
            refresh_token=Token(value=refresh_token)
        )

    def refresh_jwt_session(self, refresh_token: Token, fingerprint: Fingerprint) -> AuthDetails:
        cur_session = self.session_storage.get(refresh_token.value)
        self.session_storage.delete(refresh_token.value)
        if cur_session.fingerprint != fingerprint:
            raise AuthProviderError(detail='fingerprint error')
        return self.create_jwt_session(cur_session.payload, fingerprint)

    def delete_jwt_session(self, refresh_token: Token) -> None:
        self.session_storage.delete(refresh_token.value)

    def verify_jwt_token(self, access_token: Token) -> AuthPayload:
        try:
            claims = jwt.decode(access_token.value, self.config.secret, algorithms='HS256',
                                options={"verify_signature": True})
        except jwt.InvalidTokenError:
            raise AuthProviderError(detail='verify jwt token error')
        return AuthPayload(user_id=ID(int(claims['user_id'])))

    def generate_password_hash(self, password: str) -> HashedPassword:
        hash = SHA256.new(data=password.encode())
        return HashedPassword(hash.hexdigest())
