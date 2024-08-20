from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from core.user.schema.user import UserSchema, UserRole
from repository.sqlalchemy.model.base import Base
from core.utils.types import Email, HashedPassword, UserName, ID


class UserORM(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)

    def to_schema(self) -> UserSchema:
        return UserSchema(
            id=ID(self.id),
            login=Email(self.login),
            hashed_password=HashedPassword(self.hashed_password),
            role=UserRole(self.role),
            name=UserName(self.name)
        )
