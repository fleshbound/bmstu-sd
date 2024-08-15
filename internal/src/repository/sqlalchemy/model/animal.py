from datetime import datetime

from sqlalchemy import ForeignKey, String, DateTime, Float, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from core.animal.schema.animal import AnimalSchema
from repository.sqlalchemy.database.database import Base
from core.utils.types import Sex, AnimalName, Datetime, Weight, Height, Length, ID


class AnimalORM(Base):
    __tablename__ = "animal"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(column="user.id"))
    breed_id: Mapped[int] = mapped_column(ForeignKey(column="breed.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    birth_dt: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    sex: Mapped[str] = mapped_column(String, nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    height: Mapped[float] = mapped_column(Float, nullable=False)
    length: Mapped[float] = mapped_column(Float, nullable=False)
    has_defects: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_multicolor: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def to_schema(self) -> AnimalSchema:
        return AnimalSchema(
            id=ID(self.id),
            user_id=ID(self.user_id),
            breed_id=ID(self.breed_id),
            name=AnimalName(self.name),
            birth_dt=Datetime(self.birth_dt),
            sex=Sex(self.sex),
            weight=Weight(self.weight),
            height=Height(self.height),
            length=Length(self.length),
            has_defects=self.has_defects,
            is_multicolor=self.is_multicolor,
            is_archived=self.is_archived
        )
