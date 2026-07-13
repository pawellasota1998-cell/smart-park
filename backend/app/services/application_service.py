from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    ParkingApplicationAccessDeniedError,
    ParkingApplicationCannotBeEditedError,
    ParkingApplicationNotFoundError,
)
from app.models.enums import ApplicationStatus
from app.models.parking_application import ParkingApplication
from app.models.user import User
from app.repositories.application_repository import (
    ParkingApplicationRepository,
)
from app.schemas.application import (
    ParkingApplicationCreate,
    ParkingApplicationUpdate,
)

EDITABLE_STATUSES = {
    ApplicationStatus.PENDING,
    ApplicationStatus.NEEDS_CHANGES,
}


class ApplicationService:
    def __init__(
        self,
        repository: ParkingApplicationRepository,
    ) -> None:
        self._repository = repository

    def create_application(
        self,
        db: Session,
        *,
        current_user: User,
        application_data: ParkingApplicationCreate,
    ) -> ParkingApplication:
        try:
            application = self._repository.create(
                db,
                user_id=current_user.id,
                registration_number=application_data.registration_number,
                preferred_floor=application_data.preferred_floor,
            )
            db.commit()
            db.refresh(application)

        except SQLAlchemyError:
            db.rollback()
            raise

        return application

    def list_my_applications(
        self,
        db: Session,
        *,
        current_user: User,
    ) -> list[ParkingApplication]:
        return self._repository.list_by_user_id(
            db,
            current_user.id,
        )

    def get_my_application(
        self,
        db: Session,
        *,
        current_user: User,
        application_id: int,
    ) -> ParkingApplication:
        application = self._repository.get_by_id(
            db,
            application_id,
        )

        if application is None:
            raise ParkingApplicationNotFoundError

        if application.user_id != current_user.id:
            raise ParkingApplicationAccessDeniedError

        return application

    def update_my_application(
        self,
        db: Session,
        *,
        current_user: User,
        application_id: int,
        application_data: ParkingApplicationUpdate,
    ) -> ParkingApplication:
        application = self.get_my_application(
            db,
            current_user=current_user,
            application_id=application_id,
        )

        if application.status not in EDITABLE_STATUSES:
            raise ParkingApplicationCannotBeEditedError

        update_data = application_data.model_dump(
            exclude_unset=True,
        )

        if not update_data:
            return application

        new_status = application.status

        if application.status == ApplicationStatus.NEEDS_CHANGES:
            new_status = ApplicationStatus.PENDING

        try:
            updated_application = self._repository.update(
                db,
                application,
                registration_number=update_data.get("registration_number"),
                preferred_floor=update_data.get("preferred_floor"),
                status=new_status,
                supervisor_comment=None,
            )
            db.commit()
            db.refresh(updated_application)

        except SQLAlchemyError:
            db.rollback()
            raise

        return updated_application
