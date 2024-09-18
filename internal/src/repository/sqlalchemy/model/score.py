import datetime

from pydantic import NonNegativeInt
from sqlalchemy import ForeignKey, Boolean, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from core.show.schema.score import ScoreSchema
from core.utils.types import ID, Datetime, ScoreValue
from repository.sqlalchemy.model.base import Base


class ScoreORM(Base):
    __tablename__ = 'score'

    id: Mapped[NonNegativeInt] = mapped_column(primary_key=True)
    animalshow_id: Mapped[NonNegativeInt] = mapped_column(ForeignKey(column='animalshow.id'), nullable=False)
    usershow_id: Mapped[NonNegativeInt] = mapped_column(ForeignKey(column='usershow.id'), nullable=False)
    value: Mapped[NonNegativeInt] = mapped_column(Integer, nullable=False)
    dt_created: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def to_schema(self) -> ScoreSchema:
        return ScoreSchema(
            id=ID(self.id),
            animalshow_id=ID(self.animalshow_id),
            usershow_id=ID(self.usershow_id),
            dt_created=Datetime(self.dt_created),
            value=ScoreValue(self.value),
            is_archived=self.is_archived
        )
