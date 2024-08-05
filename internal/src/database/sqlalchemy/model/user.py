from sqlalchemy import Boolean, String
from sqlalchemy.orm import mapped_column, Mapped

from core.user.schema.user import UserSchema
from database.sqlalchemy.database import Base
from utils.types import Email, HashedPassword, Role, UserName, ID


class UserORM(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def to_schema(self) -> UserSchema:
        return UserSchema(
            id=ID(value=self.id),
            login=Email(value=self.login),
            hashed_password=HashedPassword(value=self.hashed_password),
            role=Role(value=self.role),
            name=UserName(value=self.name),
            is_archived=self.is_archived
        )
