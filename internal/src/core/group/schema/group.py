import enum

from pydantic import BaseModel

from utils.types import GroupName, ID


class GroupSchema(BaseModel):
    id: ID
    name: GroupName


class GroupSchemaCreate(BaseModel):
    name: GroupName


class GroupSchemaUpdate(BaseModel):
    id: ID
    name: GroupName


class GroupSchemaUpdateBody(BaseModel):
    name: GroupName
    

class GroupDeleteStatus(str, enum.Enum):
    deleted = "deleted"


class GroupSchemaDelete(BaseModel):
    id: ID
    status: GroupDeleteStatus = GroupDeleteStatus.deleted
