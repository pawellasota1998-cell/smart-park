from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Enum,
    Identity,
    Integer,
    Unicode,
    func,
    text,
)
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import UserRole

if TYPE_CHECKING:
    from app.models.parking_application import ParkingApplication


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, Identity(start=1, increment=1), primary_key=True
    )
    email: Mapped[str] = mapped_column(Unicode(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(Unicode(255), nullable=True)
    first_name: Mapped[str] = mapped_column(Unicode(100), nullable=False)
    last_name: Mapped[str] = mapped_column(Unicode(100), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            name="user_role",
            native_enum=False,
            create_constraint=True,
            values_callable=lambda enum_class: [number.value for number in enum_class],
            length=20,
        ),
        nullable=False,
        default=UserRole.USER,
        server_default=text("'USER'"),
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=text("1")
    )
    created_at: Mapped[datetime] = mapped_column(
        DATETIME2(precision=6),
        nullable=False,
        server_default=text("SYSUTCDATETIME()"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME2(precision=6),
        nullable=False,
        server_default=text("SYSUTCDATETIME()"),
        onupdate=func.sysutcdatetime(),
    )
    applications: Mapped[list[ParkingApplication]] = relationship(
        back_populates="user", foreign_keys="ParkingAppliaction.user_id"
    )
    reviewed_applications: Mapped[list[ParkingApplication]] = relationship(
        back_populates="reviewed_by",
        foreign_keys="ParkingAppliaction.reviewed_by_user_id",
    )
