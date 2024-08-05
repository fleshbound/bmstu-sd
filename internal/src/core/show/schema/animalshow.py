from pydantic import BaseModel

from utils.types import ID


class AnimalShowSchema(BaseModel):
    id: ID
    animal_id: ID
    show_id: ID
    is_archived: bool


class AnimalShowSchemaCreate(BaseModel):
    animal_id: ID
    show_id: ID
    is_archived: bool


class AnimalShowSchemaUpdate(BaseModel):
    id: ID
    is_archived: bool


class AnimalShowSchemaUpdateBody(BaseModel):
    is_archived: bool
