from datetime import datetime

from sqlalchemy import ForeignKey, String, DateTime, Float, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from core.animal.schema.animal import AnimalSchema
from database.database import Base
from utils.types import Sex, AnimalName, Datetime, ProlixityIndex, Weight, Height, Length, ID


class AnimalORM(Base):
    __tablename__ = "animal"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(column="user.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    birth_dt: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    sex: Mapped[str] = mapped_column(String, nullable=False)
    prolixity_index: Mapped[float] = mapped_column(Float, nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    height: Mapped[float] = mapped_column(Float, nullable=False)
    length: Mapped[float] = mapped_column(Float, nullable=False)
    has_defects: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_multicolor: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def to_schema(self) -> AnimalSchema:
        return AnimalSchema(
            id=ID(value=self.id),
            user_id=ID(value=self.user_id),
            name=AnimalName(value=self.name),
            birth_dt=Datetime(value=self.birth_dt),
            sex=Sex(value=self.sex),
            prolixity_index=ProlixityIndex(value=self.prolixity_index),
            weight=Weight(value=self.weight),
            height=Height(value=self.height),
            length=Length(value=self.length),
            has_defects=self.has_defects,
            is_multicolor=self.is_multicolor,
            is_archived=self.is_archived
        )
