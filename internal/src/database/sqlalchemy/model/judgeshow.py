from pydantic import NonNegativeInt
from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from core.show.schema.judgeshow import JudgeShowSchema
from database.sqlalchemy.database import Base
from utils.types import ID


class JudgeShowORM(Base):
    __tablename__ = 'judgeshow'

    id: Mapped[NonNegativeInt] = mapped_column(primary_key=True)
    user_id: Mapped[NonNegativeInt] = mapped_column(ForeignKey(column='user.id'), nullable=False)
    show_id: Mapped[NonNegativeInt] = mapped_column(ForeignKey(column='show.id'), nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False)
    
    def to_schema(self) -> JudgeShowSchema:
        return JudgeShowSchema(
            id=ID(value=self.id),
            show_id=ID(value=self.show_id),
            user_id=ID(value=self.user_id),
            is_archived=self.is_archived
        )
