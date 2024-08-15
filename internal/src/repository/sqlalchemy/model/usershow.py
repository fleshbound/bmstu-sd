from pydantic import NonNegativeInt
from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from core.show.schema.usershow import UserShowSchema
from repository.sqlalchemy.database.database import Base
from core.utils.types import ID


class UserShowORM(Base):
    __tablename__ = 'usershow'

    id: Mapped[NonNegativeInt] = mapped_column(primary_key=True)
    user_id: Mapped[NonNegativeInt] = mapped_column(ForeignKey(column='user.id'), nullable=False)
    show_id: Mapped[NonNegativeInt] = mapped_column(ForeignKey(column='show.id'), nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False)
    
    def to_schema(self) -> UserShowSchema:
        return UserShowSchema(
            id=ID(self.id),
            show_id=ID(self.show_id),
            user_id=ID(self.user_id),
            is_archived=self.is_archived
        )
