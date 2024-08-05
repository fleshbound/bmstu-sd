from pydantic import BaseModel

from utils.types import ID


class JudgeShowSchema(BaseModel):
    id: ID
    user_id: ID
    show_id: ID
    is_archived: bool


class JudgeShowSchemaCreate(BaseModel):
    user_id: ID
    show_id: ID
    is_archived: bool


class JudgeShowSchemaUpdate(BaseModel):
    id: ID
    is_archived: bool


class JudgeShowSchemaUpdateBody(BaseModel):
    is_archived: bool
