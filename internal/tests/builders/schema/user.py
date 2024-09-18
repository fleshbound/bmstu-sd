from core.user.schema.user import UserSchema, UserRole
from core.utils.types import Email, ID, HashedPassword, UserName


class UserSchemaBuilder:
    _id: int
    _email: str
    _hashed_password: str
    _name: str
    _role: str

    TEST_ID: int = 1
    TEST_EMAIL: str = 'coolemail@mail.ru'
    TEST_HASHED_PASSWORD: str = 'password'
    TEST_NAME: str = 'Cool Bob'
    TEST_ROLE: str = 'breeder'

    def build(self) -> UserSchema:
        return UserSchema(
            id=ID(self._id),
            email=Email(self._email),
            hashed_password=HashedPassword(self._hashed_password),
            role=UserRole(self._role),
            name=UserName(self._name)
        )

    def with_id(self, id: int):
        self._id = id
        return self

    def with_name(self, name: str):
        self._name = name
        return self

    def with_email(self, email: str):
        self._email = email
        return self

    def with_role(self, role: str):
        self._role = role
        return self

    def with_hashed_password(self, hashed_password: str):
        self._hashed_password = hashed_password
        return self

    def with_test_values(self):
        self._id = self.TEST_ID
        self._email = self.TEST_EMAIL
        self._name = self.TEST_NAME
        self._role = self.TEST_ROLE
        self._hashed_password = self.TEST_HASHED_PASSWORD
        return self

    def from_object(self, object: UserSchema):
        self._id = object.id.value
        self._email = object.email.value
        self._name = object.name.value
        self._role = object.role.value
        self._hashed_password = object.hashed_password.value
        return self
