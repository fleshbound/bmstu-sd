from pydantic import BaseModel, PositiveFloat

from utils.types import ID, Weight, Height, ProlixityIndex, Country


class StandardSchemaCreate(BaseModel):
    breed_id: ID
    country: Country
    weight: Weight
    height: Height
    has_defects: bool
    is_multi_color: bool
    prolixity_index: ProlixityIndex
    weight_delta_percent: PositiveFloat
    height_delta_percent: PositiveFloat
    prolixity_index_delta_percent: PositiveFloat


class StandardSchema(BaseModel):
    id: ID
    breed_id: ID
    country: Country
    weight: Weight
    height: Height
    has_defects: bool
    is_multi_color: bool
    prolixity_index: ProlixityIndex
    weight_delta_percent: PositiveFloat
    height_delta_percent: PositiveFloat
    prolixity_index_delta_percent: PositiveFloat

    @classmethod
    def from_create(cls, other: StandardSchemaCreate):
        return cls(
            id=ID(0),
            breed_id=other.breed_id,
            country=other.country,
            weight=other.weight,
            height=other.height,
            has_defects=other.bool,
            is_multi_color=other.bool,
            prolixity_index=other.prolixity_index,
            weight_delta_percent=other.weight_delta_percent,
            height_delta_percent=other.height_delta_percent,
            prolixity_index_delta_percent=other.prolixity_index_delta_percent
        )


class StandardSchemaDeleteResponse(BaseModel):
    status: str = "deleted"
    id: ID

