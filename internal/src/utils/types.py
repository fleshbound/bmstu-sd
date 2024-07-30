from dataclasses import dataclass
import datetime
import enum
from typing import Type

from pydantic import NonNegativeFloat, NonNegativeInt, EmailStr


@enum.unique
class Sex(str, enum.Enum):
    female = "F"
    male = "M"


@enum.unique
class Role(str, enum.Enum):
    admin = "admin"
    guest = "guest"
    breeder = "breeder"
    judge = "judge"


@dataclass
class UserName:
    value: str

    def __eq__(self, other) -> bool:
        if not isinstance(other, UserName):
            return False
        return other.value == self.value

    @property
    def val(self):
        return self.value


@dataclass
class Email:
    value: EmailStr

    def __eq__(self, other) -> bool:
        if not isinstance(other, UserName):
            return False
        return other.value == self.value

    @property
    def val(self):
        return self.value


@dataclass
class HashedPassword:
    value: str

    def __eq__(self, other) -> bool:
        if not isinstance(other, UserName):
            return False
        return other.value == self.value

    @property
    def val(self):
        return self.value


@dataclass
class AnimalName:
    value: str

    def __eq__(self, other) -> bool:
        if not isinstance(other, AnimalName):
            return False
        return other.value == self.value

    @property
    def val(self):
        return self.value


@dataclass(frozen=True)
class ID:
    value: NonNegativeInt

    def __eq__(self, other) -> bool:
        if not isinstance(other, ID):
            return False
        return other.value == self.value

    def __gt__(self, other) -> bool:
        return self.value > other.value

    @property
    def val(self):
        return self.value


@dataclass(frozen=True)
class Datetime:
    value: datetime.datetime

    def __eq__(self, other) -> bool:
        if not isinstance(other, Datetime):
            return False
        return other.value == self.value

    def __gt__(self, other) -> bool:
        return self.value > other.value

    @property
    def val(self):
        return self.value


@dataclass
class Weight:
    value: NonNegativeFloat

    def __eq__(self, other) -> bool:
        if not isinstance(other, Weight):
            return False
        return other.value == self.value

    def __gt__(self, other) -> bool:
        return self.value > other.value

    @property
    def val(self):
        return self.value


@dataclass
class Height:
    value: NonNegativeFloat

    def __eq__(self, other) -> bool:
        if not isinstance(other, Height):
            return False
        return other.value == self.value

    def __gt__(self, other) -> bool:
        return self.value > other.value

    @property
    def val(self):
        return self.value


@dataclass
class Length:
    value: NonNegativeFloat

    def __eq__(self, other) -> bool:
        if not isinstance(other, Length):
            return False
        return other.value == self.value

    def __gt__(self, other) -> bool:
        return self.value > other.value

    @property
    def val(self):
        return self.value


@dataclass
class ProlixityIndex:
    value: NonNegativeFloat

    def __eq__(self, other) -> bool:
        if not isinstance(other, ProlixityIndex):
            return False
        return other.value == self.value

    def __gt__(self, other) -> bool:
        return self.value > other.value

    @property
    def val(self):
        return self.value
