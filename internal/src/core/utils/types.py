import datetime
import enum
from dataclasses import dataclass

from pydantic import NonNegativeFloat, NonNegativeInt, EmailStr


@enum.unique
class Sex(str, enum.Enum):
    female = "F"
    male = "M"


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


@dataclass
class Weight:
    value: NonNegativeFloat

    def __eq__(self, other) -> bool:
        if not isinstance(other, Weight):
            return False
        return other.value == self.value

    def __gt__(self, other) -> bool:
        return self.value > other.value

    def __mul__(self, other: float):
        return Weight(self.value * other)

    def __sub__(self, other):
        return Weight(self.value - other.value)


@dataclass
class Height:
    value: NonNegativeFloat

    def __eq__(self, other) -> bool:
        if not isinstance(other, Height):
            return False
        return other.value == self.value

    def __gt__(self, other) -> bool:
        return self.value > other.value

    def __mul__(self, other: float):
        return Weight(self.value * other)

    def __sub__(self, other):
        return Height(self.value - other.value)


@dataclass
class Length:
    value: NonNegativeFloat

    def __eq__(self, other) -> bool:
        if not isinstance(other, Length):
            return False
        return other.value == self.value

    def __gt__(self, other) -> bool:
        return self.value > other.value

    def __mul__(self, other: float):
        return Weight(self.value * other)

    def __sub__(self, other):
        return Length(self.value - other.value)
