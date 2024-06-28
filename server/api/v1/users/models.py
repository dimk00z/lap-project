from datetime import date

from litestar.contrib.sqlalchemy.base import UUIDAuditBase
from passlib.hash import bcrypt
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class User(UUIDAuditBase):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    username = mapped_column(
        String(30),
        unique=True,
        index=True,
        primary_key=False,
    )
    password_hash: Mapped[str]
    full_name: Mapped[str]
    birthdate: Mapped[date]
    avatar_url: Mapped[str]

    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, str(self.password_hash))
