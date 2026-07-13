import re
from datetime import datetime
from math import ceil

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.enums import ApplicationStatus

REGISTRATION_NUMBER_PATTERN = re.compile(
    r"^[A-Z0-9]{4,10}$",
)


def normalize_registration_number(value: str) -> str:
    return value.strip().upper().replace(" ", "").replace("-", "")


class ParkingApplicationCreate(BaseModel):
    registration_number: str = Field(
        min_length=4,
        max_length=15,
    )

    preferred_floor: int = Field(
        ge=-5,
        le=20,
    )

    @field_validator("registration_number")
    @classmethod
    def validate_registration_number(cls, value: str) -> str:
        normalized_value = normalize_registration_number(value)

        if not REGISTRATION_NUMBER_PATTERN.fullmatch(normalized_value):
            raise ValueError("Registration number must contain 4-10 letters or digits.")

        return normalized_value


class ParkingApplicationUpdate(BaseModel):
    registration_number: str | None = Field(
        default=None,
        min_length=4,
        max_length=15,
    )

    preferred_floor: int | None = Field(
        default=None,
        ge=-5,
        le=20,
    )

    @field_validator("registration_number")
    @classmethod
    def validate_registration_number(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return value

        normalized_value = normalize_registration_number(value)

        if not REGISTRATION_NUMBER_PATTERN.fullmatch(normalized_value):
            raise ValueError("Registration number must contain 4-10 letters or digits.")

        return normalized_value


class ParkingApplicationRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    user_id: int
    registration_number: str
    preferred_floor: int
    status: ApplicationStatus
    supervisor_comment: str | None
    reviewed_by_user_id: int | None
    reviewed_at: datetime | None
    created_at: datetime
    updated_at: datetime


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int


class ParkingApplicationPage(BaseModel):
    items: list[ParkingApplicationRead]
    pagination: PaginationMeta


class SupervisorDecisionRequest(BaseModel):
    supervisor_comment: str | None = Field(
        default=None,
        max_length=1000,
    )

    @field_validator("supervisor_comment")
    @classmethod
    def strip_optional_comment(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return value

        normalized_value = value.strip()

        return normalized_value or None


class SupervisorRequestChangesRequest(BaseModel):
    supervisor_comment: str = Field(
        min_length=1,
        max_length=1000,
    )

    @field_validator("supervisor_comment")
    @classmethod
    def strip_required_comment(cls, value: str) -> str:
        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError("Supervisor comment is required.")

        return normalized_value


def build_pagination_meta(
    *,
    page: int,
    page_size: int,
    total_items: int,
) -> PaginationMeta:
    return PaginationMeta(
        page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=ceil(total_items / page_size) if total_items else 0,
    )
