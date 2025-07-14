from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import types

from .base import Base


class AuthUser(Base):
    """
    админ
    """
    __tablename__ = "auth_user"

    uuid: Mapped[UUID] = mapped_column(
        types.UUID,
        primary_key=True,
    )
    login: Mapped[str] = mapped_column(
        types.String,
        unique=True,
    )
    salt: Mapped[bytes] = mapped_column(types.LargeBinary)
    password_hash: Mapped[bytes] = mapped_column(types.LargeBinary)


class Permission(Base):
    """Разрешения - например на добавление товара в склад итд"""
    __tablename__ = "rbac_permission"
    name: Mapped[str] = mapped_column(primary_key=True)
