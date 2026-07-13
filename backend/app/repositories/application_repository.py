from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import ApplicationStatus
from app.models.parking_application import ParkingApplication


class ParkingApplicationRepository:
    def get_by_id(
        self,
        db: Session,
        application_id: int,
    ) -> ParkingApplication | None:
        return db.get(
            ParkingApplication,
            application_id,
        )

    def list_by_user_id(
        self,
        db: Session,
        user_id: int,
    ) -> list[ParkingApplication]:
        statement = (
            select(ParkingApplication)
            .where(ParkingApplication.user_id == user_id)
            .order_by(ParkingApplication.created_at.desc())
        )

        return list(db.scalars(statement).all())

    def create(
        self,
        db: Session,
        *,
        user_id: int,
        registration_number: str,
        preferred_floor: int,
    ) -> ParkingApplication:
        application = ParkingApplication(
            user_id=user_id,
            registration_number=registration_number,
            preferred_floor=preferred_floor,
            status=ApplicationStatus.PENDING,
        )

        db.add(application)
        db.flush()

        return application

    def update(
        self,
        db: Session,
        application: ParkingApplication,
        *,
        registration_number: str | None = None,
        preferred_floor: int | None = None,
        status: ApplicationStatus | None = None,
        supervisor_comment: str | None = None,
    ) -> ParkingApplication:
        if registration_number is not None:
            application.registration_number = registration_number

        if preferred_floor is not None:
            application.preferred_floor = preferred_floor

        if status is not None:
            application.status = status

        if supervisor_comment is not None:
            application.supervisor_comment = supervisor_comment

        db.flush()

        return application
