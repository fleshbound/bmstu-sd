from auth_provider.utils.exceptions import AuthProviderError
from core.auth.provider.auth import IAuthProvider
from core.auth.schema.auth import AuthPayload, AuthDetails
from core.utils.types import HashedPassword, ID, Token, Fingerprint


class MockedAuthProvider(IAuthProvider):
    _do_verify: bool
    _fingerprint_ok: bool

    def __init__(self, do_verify: bool, fingerprint_ok: bool):
        self._do_verify = do_verify
        self._fingerprint_ok = fingerprint_ok

    def create_jwt_session(self, payload: AuthPayload, fingerprint: Fingerprint) -> AuthDetails:
        return AuthDetails(access_token=Token(value='access123'), refresh_token=Token(value='refresh123'))

    def refresh_jwt_session(self, refresh_token: Token, fingerprint: Fingerprint) -> AuthDetails:
        if not self._fingerprint_ok:
            raise AuthProviderError(detail='fingerprint error')
        return AuthDetails(access_token=Token(value='access123'), refresh_token=refresh_token)

    def delete_jwt_session(self, refresh_token: Token) -> None:
        return None

    def verify_jwt_token(self, access_token: Token) -> AuthPayload:
        if not self._do_verify:
            raise AuthProviderError(detail='verify jwt token error')
        return AuthPayload(user_id=ID(0))

    def generate_password_hash(self, password: str) -> HashedPassword:
        return HashedPassword(password)
