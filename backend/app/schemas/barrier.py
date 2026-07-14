from pydantic import BaseModel, Field, field_validator

from app.core.registration_number import validate_registration_number


class BarrierAccessRequest(BaseModel):
    registration_number: str = Field(
        min_length=4,
        max_length=15,
    )

    @field_validator("registration_number")
    @classmethod
    def validate_registration_number_field(cls, value: str) -> str:
        return validate_registration_number(value)


class BarrierAccessResponse(BaseModel):
    registration_number: str
    access_granted: bool
