from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Identity, Integer, Unicode, text
from sqlalchemy.dialects.mssql import DATETIME2, UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(start=1, increment=1),
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    jti: Mapped[UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True),
        nullable=False,
        unique=True,
    )

    token_hash: Mapped[str] = mapped_column(
        Unicode(64),
        nullable=False,
        unique=True,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DATETIME2(precision=6),
        nullable=False,
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        DATETIME2(precision=6),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DATETIME2(precision=6),
        nullable=False,
        server_default=text("SYSUTCDATETIME()"),
    )

    user: Mapped[User] = relationship(
        back_populates="refresh_tokens",
    )
