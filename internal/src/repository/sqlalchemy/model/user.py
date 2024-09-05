from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from internal.src.core.user.schema.user import UserSchema, UserRole
from internal.src.core.utils.types import Email, HashedPassword, UserName, ID
from internal.src.repository.sqlalchemy.model.base import Base


class UserORM(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)

    def to_schema(self) -> UserSchema:
        return UserSchema(
            id=ID(self.id),
            email=Email(self.email),
            hashed_password=HashedPassword(self.hashed_password),
            role=UserRole(self.role),
            name=UserName(self.name)
        )
