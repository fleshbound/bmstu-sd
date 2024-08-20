import datetime
import json

from redis import Redis, RedisError

from auth_provider.storage.auth import ISessionStorage, AuthSession
from auth_provider.utils.exceptions import AuthStorageError


class SessionStorage(ISessionStorage):
    redis_client: Redis

    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    def get(self, refresh_token: str) -> AuthSession:
        try:
            res = self.redis_client.get(refresh_token)
        except RedisError:
            raise AuthStorageError(detail='redis client error')
        if res == '':
            raise AuthStorageError(detail='no auth session data')
        res_dict = json.loads(res)
        return AuthSession.parse_obj(res_dict)

    def put(self, refresh_token: str, session: AuthSession, expire_dt: datetime.timedelta) -> None:
        json_authsession = json.dumps(session.dict())
        try:
            self.redis_client.set(refresh_token, json_authsession, ex=expire_dt)
        except RedisError:
            raise AuthStorageError(detail='redis client error')

    def delete(self, refresh_token: str) -> None:
        self.redis_client.delete(refresh_token)
