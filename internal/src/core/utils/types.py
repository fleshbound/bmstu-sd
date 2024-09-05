import datetime
import enum
from dataclasses import dataclass, field

from pydantic import NonNegativeInt, EmailStr, PositiveFloat, BaseModel


@enum.unique
class Sex(str, enum.Enum):
    female = "male"
    male = "female"


@dataclass
class UserName:
    value: str

    def __eq__(self, other) -> bool:
        if not isinstance(other, UserName):
            return False
        return other.value == self.value


@dataclass
class BreedName:
    value: str

    def __eq__(self, other) -> bool:
        if not isinstance(other, BreedName):
            return False
        return other.value == self.value


@dataclass
class SpeciesName:
    value: str

    def __eq__(self, other) -> bool:
        if not isinstance(other, SpeciesName):
            return False
        return other.value == self.value


@dataclass
class GroupName:
    value: str

    def __eq__(self, other) -> bool:
        if not isinstance(other, GroupName):
            return False
        return other.value == self.value


@dataclass
class Country:
    value: str

    def __eq__(self, other) -> bool:
        if not isinstance(other, Country):
            return False
        return other.value == self.value


@dataclass
class ShowName:
    value: str

    def __eq__(self, other) -> bool:
        if not isinstance(other, ShowName):
            return False
        return other.value == self.value


@dataclass
class Email:
    value: EmailStr

    def __eq__(self, other) -> bool:
        if not isinstance(other, UserName):
            return False
        return other.value == self.value


@dataclass
class HashedPassword:
    value: str

    def __eq__(self, other) -> bool:
        if not isinstance(other, UserName):
            return False
        return other.value == self.value


@dataclass
class AnimalName:
    value: str

    def __eq__(self, other) -> bool:
        if not isinstance(other, AnimalName):
            return False
        return other.value == self.value


@dataclass
class ID:
    value: NonNegativeInt

    def __eq__(self, other) -> bool:
        if not isinstance(other, ID):
            return False
        return other.value == self.value

    def __gt__(self, other) -> bool:
        return self.value > other.value
    
    def __le__(self, other) -> bool:
        return self.value < other.value

    def eq_int(self, n: int) -> bool:
        return n == self.value


@dataclass
class Datetime:
    value: datetime.datetime

    def __eq__(self, other) -> bool:
        if not isinstance(other, Datetime):
            return False
        return other.value == self.value

    def __gt__(self, other) -> bool:
        return self.value > other.value
    
    def __le__(self, other) -> bool:
        return self.value < other.value


@dataclass
class Weight:
    value: PositiveFloat

    def __eq__(self, other) -> bool:
        if not isinstance(other, Weight):
            return False
        return other.value == self.value

    def __gt__(self, other) -> bool:
        return self.value > other.value
    
    def __le__(self, other) -> bool:
        return self.value < other.value

    def __mul__(self, other: float):
        return Weight(self.value * other)

    def __sub__(self, other):
        return Weight(self.value - other.value)

    def __truediv__(self, other):
        return Weight(self.value / other.value)


@dataclass
class Height:
    value: PositiveFloat

    def __eq__(self, other) -> bool:
        if not isinstance(other, Height):
            return False
        return other.value == self.value

    def __gt__(self, other) -> bool:
        return self.value > other.value
    
    def __le__(self, other) -> bool:
        return self.value < other.value

    def __mul__(self, other: float):
        return Weight(self.value * other)

    def __sub__(self, other):
        return Height(self.value - other.value)


@dataclass
class Length:
    value: PositiveFloat

    def __eq__(self, other) -> bool:
        if not isinstance(other, Length):
            return False
        return other.value == self.value

    def __gt__(self, other) -> bool:
        return self.value > other.value
    
    def __le__(self, other) -> bool:
        return self.value < other.value

    def __mul__(self, other: float):
        return Weight(self.value * other)

    def __sub__(self, other):
        return Length(self.value - other.value)


class Token(BaseModel):
    value: str

    def __eq__(self, other) -> bool:
        if not isinstance(other, Token):
            return False
        return other.value == self.value

    def __gt__(self, other) -> bool:
        return self.value > other.value


class Fingerprint(BaseModel):
    value: str

    def __eq__(self, other) -> bool:
        if not isinstance(other, Fingerprint):
            return False
        return other.value == self.value

    def __gt__(self, other) -> bool:
        return self.value > other.value


MAX_SCORE_VALUE = 5


@dataclass(frozen=True)
class ScoreValue:
    value: NonNegativeInt
    min: NonNegativeInt = field(init=False)
    max: NonNegativeInt = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "min", 0)
        object.__setattr__(self, "max", MAX_SCORE_VALUE)

        if self.value > self.max or self.value < self.min:
            raise ValueError("Value of ScoreValue must be greater than " + str(self.min)
                             + " and less than " + str(self.max))

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
        return Score(self.value + other.value)

    def __gt__(self, other) -> bool:
        return self.value > other.value

    def __le__(self, other) -> bool:
        return self.value < other.value

    @classmethod
    def from_other(cls, other):
        return Score(other.value)
