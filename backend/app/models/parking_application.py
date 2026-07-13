from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Enum,
    ForeignKey,
    Identity,
    Index,
    Integer,
    SmallInteger,
    Unicode,
    func,
    text,
)
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import ApplicationStatus

if TYPE_CHECKING:
    from app.models.user import User


class ParkingApplication(Base):
    __tablename__ = "parking_applications"

    __table_args__ = (
        Index(
            "ix_parking_applications_registration_status",
            "registration_number",
            "status",
        ),
        Index(
            "ix_parking_applications_status_created_at",
            "status",
            "created_at",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    registration_number: Mapped[str] = mapped_column(
        Unicode(15),
        nullable=False,
    )
    preferred_floor: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(
            ApplicationStatus,
            name="application_status",
            native_enum=False,
            create_constraint=True,
            values_callable=lambda enum_class: [number.value for number in enum_class],
            length=20,
        ),
        nullable=False,
        default=ApplicationStatus.PENDING,
        server_default=text("'PENDING'"),
    )
    supervisor_comment: Mapped[str | None] = mapped_column(
        Unicode(1000),
        nullable=True,
    )
    reviewed_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(
        DATETIME2(precision=6),
        nullable=True,
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
    user: Mapped[User] = relationship(back_populates="applications", foreign_keys=[user_id])
    reviewed_by: Mapped[User] = relationship(back_populates="reviewed_applications", foreign_keys=[reviewed_by_user_id])
