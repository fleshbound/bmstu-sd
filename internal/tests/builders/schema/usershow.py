from internal.src.core.show.schema.usershow import UserShowSchema
from internal.src.core.utils.types import ID


class UserShowSchemaBuilder:
    _id: int
    _user_id: int
    _show_id: int
    _is_archived: bool

    TEST_ID: int = 1
    TEST_USER_ID: int = 1
    TEST_SHOW_ID: int = 1
    TEST_IS_ARCHIVED: bool = False

    def build(self):
        return UserShowSchema(
            id=ID(self._id),
            user_id=ID(self._user_id),
            show_id=ID(self._show_id),
            is_archived=self._is_archived
        )

    def with_id(self, id: int):
        self._id = id
        return self

    def with_user_id(self, user_id: int):
        self._user_id = user_id
        return self

    def with_show_id(self, show_id: int):
        self._show_id = show_id
        return self

    def with_is_archived(self, is_archived: bool):
        self._is_archived = is_archived
        return self

    def with_test_values(self):
        self._id = self.TEST_ID
        self._show_id = self.TEST_SHOW_ID
        self._user_id = self.TEST_USER_ID
        self._is_archived = self.TEST_IS_ARCHIVED
        return self
    
    def from_object(self, other: UserShowSchema):
        self._id = other.id.value
        self._show_id = other.show_id.value
        self._user_id = other.user_id.value
        self._is_archived = other.is_archived
        return self
