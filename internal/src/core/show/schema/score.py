from dataclasses import dataclass, field
from typing import Optional

from pydantic import BaseModel, NonNegativeInt, PositiveInt, NonNegativeFloat

from utils.types import ID, Datetime


@dataclass(frozen=True)
class ScoreValue:
    value: NonNegativeInt
    min: NonNegativeInt = field(init=False)
    max: NonNegativeInt = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "min", 0)
        object.__setattr__(self, "max", 5)

        if self.value > self.max or self.value < self.min:
            raise ValueError("Value of ScoreValue must be greater than " + self.min.__str__()
                             + " and less than " + self.max.__str__())

    @classmethod
    def from_other(cls, other):
        if not isinstance(other, ScoreValue):
            raise ValueError("Parameter must be the instance of " + cls.__name__ + " class")
        return cls(other.value)


@dataclass(frozen=False)
class Score:
    value: NonNegativeInt

    @classmethod
    def from_scorevalue(cls, other: ScoreValue):
        return cls(other.value)

    def __add__(self, other):
        if not isinstance(other, Score):
            raise ValueError("Sum parameter must be the instance of " + object.__class__.__name__ + " class")
        return Score(self.value + other.value)

    def __gt__(self, other) -> bool:
        if not isinstance(other, Score):
            raise ValueError("Sum parameter must be the instance of " + object.__class__.__name__ + " class")
        return self.value > other.value

    @classmethod
    def from_other(cls, other):
        if not isinstance(other, Score):
            raise ValueError("Init parameter must be the instance of " + object.__class__.__name__ + " class")
        return Score(other.value)


class TotalScoreInfo(BaseModel):
    total: Score
    count: NonNegativeInt
    average: Optional[NonNegativeFloat]
    max_score: Optional[ScoreValue]
    min_score: Optional[ScoreValue]


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

    @classmethod
    def from_update(cls, cur, other: ScoreSchemaUpdate):
        if not isinstance(cur, ScoreSchema):
            raise ValueError("Sum parameter must be the instance of " + object.__class__.__name__ + " class")
        return cls(
            id=cur.id,
            value=cur.value,
            dt_created=cur.dt_created,
            usershow_id=cur.usershow_id,
            animalshow_id=cur.animalshow_id,
            is_archived=other.is_archived
        )
