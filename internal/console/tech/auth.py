from core.auth.schema.auth import Token
from internal.console.tech.console import UserConsoleInfo


class AuthHandler:
    def verify_auth_role(self):
        raise NotImplementedError

    def verify_auth(self):
        raise NotImplementedError

    def signin(self) -> UserConsoleInfo:
        raise NotImplementedError

    def verify_token(self, token: Token) -> bool:
        raise NotImplementedError

    def signup(self):
        raise NotImplementedError

    def logout(self):
        raise NotImplementedError
