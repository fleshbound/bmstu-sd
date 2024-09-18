from pydantic import BaseModel

from core.utils.types import ID


class UserShowSchemaCreate(BaseModel):
    user_id: ID
    show_id: ID
    is_archived: bool = False


class UserShowSchemaUpdate(BaseModel):
    id: ID
    is_archived: bool


class UserShowSchema(BaseModel):
    id: ID
    user_id: ID
    show_id: ID
    is_archived: bool
    
    @classmethod
    def from_create(cls, other: UserShowSchemaCreate):
        return cls(
            id=ID(0),
            user_id=other.user_id,
            show_id=other.show_id,
            is_archived=other.is_archived
        )

    def from_update(self, other: UserShowSchemaUpdate):
        return UserShowSchema(
            id=self.id,
            user_id=self.user_id,
            show_id=self.show_id,
            is_archived=other.is_archived
        )


class UserShowSchemaUpdateBody(BaseModel):
    is_archived: bool


class UserShowSchemaDeleted(BaseModel):
    id: ID
    status: str = "deleted"
