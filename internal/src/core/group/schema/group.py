import enum

from pydantic import BaseModel

from internal.src.core.utils.types import GroupName, ID


class GroupSchemaCreate(BaseModel):
    name: GroupName


class GroupSchemaUpdate(BaseModel):
    id: ID
    name: GroupName


class GroupSchema(BaseModel):
    id: ID
    name: GroupName

    @classmethod
    def from_create(cls, other: GroupSchemaCreate):
        return cls(
            id=ID(0),
            name=other.name
        )

    def from_update(self, other: GroupSchemaUpdate):
        return GroupSchema(
            id=other.id,
            name=other.name
        )
    

class GroupDeleteStatus(str, enum.Enum):
    deleted = "deleted"


class GroupSchemaDelete(BaseModel):
    id: ID
    status: GroupDeleteStatus = GroupDeleteStatus.deleted
