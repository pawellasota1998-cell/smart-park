from datetime import datetime
from typing import Literal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.enums import ApplicationStatus
from app.models.parking_application import ParkingApplication

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

    def list_for_supervisor(
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
        filters = []
        if application_status is not None:
            filters.append(ParkingApplication.status == application_status)
        if registration_number:
            filters.append(ParkingApplication.registration_number.contains(registration_number))

        total_statement = select(func.count()).select_from(ParkingApplication)

        if filters:
            total_statement = total_statement.where(*filters)

        total_items = db.scalar(total_statement) or 0

        sort_columns = {
            "created_at": ParkingApplication.created_at,
            "status": ParkingApplication.status,
            "registration_number": ParkingApplication.registration_number,
            "preferred_floor": ParkingApplication.preferred_floor,
        }

        sort_column = sort_columns.get(sort_by)

        order_expression = sort_column.desc() if sort_order == "desc" else sort_column.asc()
        statement = select(ParkingApplication)

        if filters:
            statement = statement.where(*filters)

        statement = statement.order_by(order_expression).offset((page - 1) * page_size).limit(page_size)

        return list(db.scalars(statement).all()), total_items

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

    def review(
        self,
        db: Session,
        application: ParkingApplication,
        *,
        status: ApplicationStatus,
        supervisor_comment: str | None,
        reviewed_by_user_id: int,
        reviewed_at: datetime,
    ) -> ParkingApplication:
        application.status = status
        application.supervisor_comment = supervisor_comment
        application.reviewed_by_user_id = reviewed_by_user_id
        application.reviewed_at = reviewed_at

        db.flush()

        return application

    def has_approved_registration_number(
        self,
        db: Session,
        *,
        registration_number: str,
    ) -> bool:
        statement = (
            select(ParkingApplication.id)
            .where(
                ParkingApplication.registration_number == registration_number,
                ParkingApplication.status == ApplicationStatus.APPROVED,
            )
            .limit(1)
        )
        return db.scalar(statement) is not None
