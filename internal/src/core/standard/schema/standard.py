from pydantic import BaseModel, PositiveFloat

<<<<<<< HEAD
<<<<<<< HEAD
from internal.src.core.utils.types import ID, Weight, Height, Length, Country, Length
||||||| parent of fb32d3b (tests arent working watahel)
from core.utils.types import ID, Weight, Height, Length, Country, Length
=======
from core.utils.types import ID, Weight, Height, Country, Length
>>>>>>> fb32d3b (tests arent working watahel)
||||||| parent of d8bdfb9 (add animal tests (init))
from core.utils.types import ID, Weight, Height, Country, Length
=======
from internal.src.core.utils.types import ID, Weight, Height, Country, Length
>>>>>>> d8bdfb9 (add animal tests (init))


class StandardSchemaCreate(BaseModel):
    breed_id: ID
    country: Country
    weight: Weight
    height: Height
    has_defects: bool
    is_multicolor: bool
    length: Length
    weight_delta_percent: PositiveFloat
    height_delta_percent: PositiveFloat
    length_delta_percent: PositiveFloat


class StandardSchema(BaseModel):
    id: ID
    breed_id: ID
    country: Country
    weight: Weight
    height: Height
    has_defects: bool
    is_multicolor: bool
    length: Length
    weight_delta_percent: PositiveFloat
    height_delta_percent: PositiveFloat
    length_delta_percent: PositiveFloat

    @classmethod
    def from_create(cls, other: StandardSchemaCreate):
        return cls(
            id=ID(0),
            breed_id=other.breed_id,
            country=other.country,
            weight=other.weight,
            height=other.height,
            has_defects=other.bool,
            is_multicolor=other.bool,
            length=other.length,
            weight_delta_percent=other.weight_delta_percent,
            height_delta_percent=other.height_delta_percent,
            length_delta_percent=other.length_delta_percent
        )


class StandardSchemaDeleteResponse(BaseModel):
    status: str = "deleted"
    id: ID

