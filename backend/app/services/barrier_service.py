from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.repositories.application_repository import (
    ParkingApplicationRepository,
)
from app.schemas.barrier import BarrierAccessRequest


@dataclass(frozen=True)
class BarrierAccessResult:
    registration_number: str
    access_granted: bool


class BarrierService:
    def __init__(
        self,
        application_repository: ParkingApplicationRepository,
    ) -> None:
        self._application_repository = application_repository

    def check_access(
        self,
        db: Session,
        *,
        request_data: BarrierAccessRequest,
    ) -> BarrierAccessResult:
        access_granted = self._application_repository.has_approved_registration_number(
            db,
            registration_number=request_data.registration_number,
        )
        return BarrierAccessResult(
            registration_number=request_data.registration_number,
            access_granted=access_granted,
        )
