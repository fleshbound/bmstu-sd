from typing import Optional

from pydantic import BaseModel, NonNegativeInt, NonNegativeFloat

from internal.src.core.utils.types import ID, Datetime, ScoreValue, Score


class TotalScoreInfo(BaseModel):
    record_id: ID
    total: Score
    count: NonNegativeInt
    average: Optional[NonNegativeFloat]
    max_score: Optional[Score]
    min_score: Optional[Score]


class AnimalShowRankingInfo(BaseModel):
    total_info: TotalScoreInfo
    rank: NonNegativeInt


class ScoreSchemaCreate(BaseModel):
    usershow_id: ID
    animalshow_id: ID
    value: ScoreValue
    dt_created: Datetime


class ScoreSchemaUpdate(BaseModel):
    id: ID
    is_archived: bool


class ScoreSchema(BaseModel):
    id: ID
    usershow_id: ID
    animalshow_id: ID
    value: ScoreValue
    is_archived: bool
    dt_created: Datetime

    @classmethod
    def from_create(cls, other: ScoreSchemaCreate):
        return cls(
            id=ID(0),
            value=other.value,
            dt_created=other.dt_created,
            usershow_id=other.usershow_id,
            animalshow_id=other.animalshow_id,
            is_archived=False
        )

    def from_update(self, other: ScoreSchemaUpdate):
        return ScoreSchema(
            id=self.id,
            value=self.value,
            dt_created=self.dt_created,
            usershow_id=self.usershow_id,
            animalshow_id=self.animalshow_id,
            is_archived=other.is_archived
        )
