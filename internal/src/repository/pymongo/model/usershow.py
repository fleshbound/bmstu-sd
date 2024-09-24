from pydantic import BaseModel, Field

from core.show.schema.usershow import UserShowSchema
from core.utils.types import ID
from repository.utils.types import PyObjectId, int_from_pyobject_id


class UserShowODM(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    user_id: int
    show_id: int
    is_archived: bool

    def to_schema(self) -> UserShowSchema:
        return UserShowSchema(
            id=ID(int_from_pyobject_id(self.id)),
            user_id=ID(self.user_id),
            show_id=ID(self.show_id),
            is_archived=self.is_archived
        )
