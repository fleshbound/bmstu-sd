from pydantic import BaseModel

from core.utils.types import ID


class AnimalShowSchemaCreate(BaseModel):
    animal_id: ID
    show_id: ID
    is_archived: bool = False


class AnimalShowSchemaUpdate(BaseModel):
    id: ID
    is_archived: bool


class AnimalShowSchema(BaseModel):
    id: ID
    animal_id: ID
    show_id: ID
    is_archived: bool

    @classmethod
    def from_create(cls, other: AnimalShowSchemaCreate):
        return cls(
            id=ID(0),
            animal_id=other.animal_id,
            show_id=other.show_id,
            is_archived=other.is_archived
        )

    def from_update(self, other: AnimalShowSchemaUpdate):
        return AnimalShowSchema(
            id=self.id,
            animal_id=self.animal_id,
            show_id=self.show_id,
            is_archived=other.is_archived
        )


class AnimalShowSchemaUpdateBody(BaseModel):
    is_archived: bool


class AnimalShowSchemaDeleted(BaseModel):
    status: str = "deleted"
    id: ID
