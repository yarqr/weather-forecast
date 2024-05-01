from typing import Optional
from uuid import UUID

from sqlalchemy import BigInteger, String, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from weather_forecast.domain.entities.user import User


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    language: Mapped[Optional[str]] = mapped_column(String(2), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)

    @classmethod
    def from_entity(cls, user: User) -> "UserModel":
        return cls(id=user.id, tg_id=user.tg_id, language=user.language, city=user.city)

    def to_entity(self) -> User:
        return User(
            id=self.id, tg_id=self.tg_id, language=self.language, city=self.city
        )
