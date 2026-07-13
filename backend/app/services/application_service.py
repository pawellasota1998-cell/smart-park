from datetime import UTC, datetime
from typing import Literal

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    ParkingApplicationAccessDeniedError,
    ParkingApplicationCannotBeEditedError,
    ParkingApplicationCannotBeReviewedError,
    ParkingApplicationNotFoundError,
    SupervisorCommentRequiredError,
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

ApplicationSortField = Literal[
    "created_at",
    "status",
    "registration_number",
    "preferred_floor",
]

SortOrder = Literal[
    "asc",
    "desc",
]

EDITABLE_STATUSES = {
    ApplicationStatus.PENDING,
    ApplicationStatus.NEEDS_CHANGES,
}
REVIEWABLE_STATUSES = {
    ApplicationStatus.PENDING,
}


def utc_now_naive() -> datetime:
    return datetime.now(
        UTC,
    ).replace(
        tzinfo=None,
    )


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

        clear_supervisor_comment = application.status == ApplicationStatus.NEEDS_CHANGES
        try:
            updated_application = self._repository.update(
                db,
                application,
                registration_number=update_data.get("registration_number"),
                preferred_floor=update_data.get("preferred_floor"),
                status=new_status,
                supervisor_comment=clear_supervisor_comment,
            )
            db.commit()
            db.refresh(updated_application)

        except SQLAlchemyError:
            db.rollback()
            raise

        return updated_application

    def list_applications_for_supervisor(
        self,
        db: Session,
        *,
        application_status: ApplicationStatus | None,
        registration_number: str | None,
        page: int,
        page_size: int,
        sort_by: ApplicationSortField,
        sort_order: SortOrder,
    ) -> tuple[list[ParkingApplication], int]:

        normalized_registration_number = (
            registration_number.strip().upper().replace(" ", "").replace("-", "") if registration_number else None
        )

        return self._repository.list_for_supervisor(
            db,
            application_status=application_status,
            registration_number=normalized_registration_number,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_order=sort_order,
        )

    def approve_application(
        self,
        db: Session,
        *,
        supervisor: User,
        application_id: int,
    ) -> ParkingApplication:
        return self._review_application(
            db,
            supervisor=supervisor,
            application_id=application_id,
            new_status=ApplicationStatus.APPROVED,
            supervisor_comment=None,
        )

    def reject_application(
        self,
        db: Session,
        *,
        supervisor: User,
        application_id: int,
        supervisor_comment: str | None,
    ) -> ParkingApplication:
        return self._review_application(
            db,
            supervisor=supervisor,
            application_id=application_id,
            new_status=ApplicationStatus.REJECTED,
            supervisor_comment=supervisor_comment,
        )

    def request_changes(
        self,
        db: Session,
        *,
        supervisor: User,
        application_id: int,
        supervisor_comment: str,
    ) -> ParkingApplication:
        if not supervisor_comment.strip():
            raise SupervisorCommentRequiredError

        return self._review_application(
            db,
            supervisor=supervisor,
            application_id=application_id,
            new_status=ApplicationStatus.NEEDS_CHANGES,
            supervisor_comment=supervisor_comment,
        )

    def _review_application(
        self,
        db: Session,
        *,
        supervisor: User,
        application_id: int,
        new_status: ApplicationStatus,
        supervisor_comment: str | None,
    ) -> ParkingApplication:
        application = self._repository.get_by_id(
            db,
            application_id,
        )

        if application is None:
            raise ParkingApplicationNotFoundError

        if application.status not in REVIEWABLE_STATUSES:
            raise ParkingApplicationCannotBeReviewedError
        try:
            reviewed_application = self._repository.review(
                db,
                application,
                status=new_status,
                supervisor_comment=supervisor_comment,
                reviewed_by_user_id=supervisor.id,
                reviewed_at=utc_now_naive(),
            )

            db.refresh(reviewed_application)
            db.commit()

        except SQLAlchemyError:
            db.rollback()
            raise
        return reviewed_application
