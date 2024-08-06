from pydantic import BaseModel

from utils.types import ID


class UserShowSchema(BaseModel):
    id: ID
    user_id: ID
    show_id: ID
    is_archived: bool


class UserShowSchemaCreate(BaseModel):
    user_id: ID
    show_id: ID
    is_archived: bool


class UserShowSchemaUpdate(BaseModel):
    id: ID
    is_archived: bool


class UserShowSchemaUpdateBody(BaseModel):
    is_archived: bool
