import datetime

from pydantic import BaseModel, Field

from core.show.schema.score import ScoreSchema
from core.utils.types import ID, Datetime, ScoreValue
from repository.utils.types import PyObjectId, int_from_pyobject_id


class ScoreORM(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    animalshow_id: int
    usershow_id: int
    value: int
    dt_created: datetime.datetime
    is_archived: bool

    def to_schema(self) -> ScoreSchema:
        return ScoreSchema(
            id=ID(int_from_pyobject_id(self.id)),
            animalshow_id=ID(self.animalshow_id),
            usershow_id=ID(self.usershow_id),
            dt_created=Datetime(self.dt_created),
            value=ScoreValue(self.value),
            is_archived=self.is_archived
        )
