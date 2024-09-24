from pydantic import BaseModel, Field

from core.group.schema.group import GroupSchema
from core.utils.types import ID, GroupName
from repository.utils.types import PyObjectId, int_from_pyobject_id


class GroupORM(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    name: str

    def to_schema(self) -> GroupSchema:
        return GroupSchema(
            id=ID(int_from_pyobject_id(self.id)),
            name=GroupName(self.name)
        )
