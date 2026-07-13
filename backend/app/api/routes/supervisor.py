from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.dependencies.roles import require_supervisor
from app.api.dependencies.services import get_application_service
from app.core.exceptions import (
    ParkingApplicationCannotBeReviewedError,
    ParkingApplicationNotFoundError,
    SupervisorCommentRequiredError,
)
from app.models.enums import ApplicationStatus
from app.models.user import User
from app.schemas.application import (
    ParkingApplicationPage,
    ParkingApplicationRead,
    SupervisorDecisionRequest,
    SupervisorRequestChangesRequest,
    build_pagination_meta,
)
from app.services.application_service import ApplicationService

router = APIRouter(
    prefix="/supervisor/applications",
    tags=["Supervisor"],
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


@router.get(
    "",
    response_model=ParkingApplicationPage,
    status_code=status.HTTP_200_OK,
    summary="List parking applications",
    description=("Returns parking applications for supervisors " "with pagination, filtering and sorting."),
)
def list_applications(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    supervisor: Annotated[
        User,
        Depends(require_supervisor),
    ],
    application_service: Annotated[
        ApplicationService,
        Depends(get_application_service),
    ],
    application_status: Annotated[
        ApplicationStatus | None,
        Query(alias="status"),
    ] = None,
    registration_number: Annotated[
        str | None,
        Query(min_length=1, max_length=15),
    ] = None,
    page: Annotated[
        int,
        Query(ge=1),
    ] = 1,
    page_size: Annotated[
        int,
        Query(ge=1, le=100),
    ] = 20,
    sort_by: ApplicationSortField = "created_at",
    sort_order: SortOrder = "desc",
) -> ParkingApplicationPage:
    del supervisor

    applications, total_items = application_service.list_applications_for_supervisor(
        db,
        application_status=application_status,
        registration_number=registration_number,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return ParkingApplicationPage(
        items=[ParkingApplicationRead.model_validate(application) for application in applications],
        pagination=build_pagination_meta(
            page=page,
            page_size=page_size,
            total_items=total_items,
        ),
    )


def _not_found_error() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "code": "PARKING_APPLICATION_NOT_FOUND",
            "message": "Parking application was not found.",
        },
    )


def _cannot_be_reviewed_error() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail={
            "code": "PARKING_APPLICATION_CANNOT_BE_REVIEWED",
            "message": ("Parking application cannot be reviewed " "in its current status."),
        },
    )


@router.patch(
    "/{application_id}/approve",
    response_model=ParkingApplicationRead,
    status_code=status.HTTP_200_OK,
    summary="Approve parking application",
    description="Approves a pending parking application.",
)
def approve_application(
    application_id: int,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    supervisor: Annotated[
        User,
        Depends(require_supervisor),
    ],
    application_service: Annotated[
        ApplicationService,
        Depends(get_application_service),
    ],
) -> ParkingApplicationRead:
    try:
        application = application_service.approve_application(
            db,
            supervisor=supervisor,
            application_id=application_id,
        )

    except ParkingApplicationNotFoundError as exc:
        raise _not_found_error() from exc

    except ParkingApplicationCannotBeReviewedError as exc:
        raise _cannot_be_reviewed_error() from exc

    return ParkingApplicationRead.model_validate(application)


@router.patch(
    "/{application_id}/reject",
    response_model=ParkingApplicationRead,
    status_code=status.HTTP_200_OK,
    summary="Reject parking application",
    description="Rejects a pending parking application.",
)
def reject_application(
    application_id: int,
    request_data: SupervisorDecisionRequest,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    supervisor: Annotated[
        User,
        Depends(require_supervisor),
    ],
    application_service: Annotated[
        ApplicationService,
        Depends(get_application_service),
    ],
) -> ParkingApplicationRead:
    try:
        application = application_service.reject_application(
            db,
            supervisor=supervisor,
            application_id=application_id,
            supervisor_comment=request_data.supervisor_comment,
        )
    except ParkingApplicationNotFoundError as exc:
        raise _not_found_error() from exc

    except ParkingApplicationCannotBeReviewedError as exc:
        raise _cannot_be_reviewed_error() from exc

    return ParkingApplicationRead.model_validate(application)


@router.patch(
    "/{application_id}/request-changes",
    response_model=ParkingApplicationRead,
    status_code=status.HTTP_200_OK,
    summary="Request application changes",
    description=("Sends a pending parking application back to the user " "with a required supervisor comment."),
)
def request_application_changes(
    application_id: int,
    request_data: SupervisorRequestChangesRequest,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    supervisor: Annotated[
        User,
        Depends(require_supervisor),
    ],
    application_service: Annotated[
        ApplicationService,
        Depends(get_application_service),
    ],
) -> ParkingApplicationRead:
    try:
        application = application_service.request_changes(
            db,
            supervisor=supervisor,
            application_id=application_id,
            supervisor_comment=request_data.supervisor_comment,
        )
    except ParkingApplicationNotFoundError as exc:
        raise _not_found_error() from exc

    except ParkingApplicationCannotBeReviewedError as exc:
        raise _cannot_be_reviewed_error() from exc
    except SupervisorCommentRequiredError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "code": "SUPERVISOR_COMMENT_REQUIRED",
                "message": "Supervisor comment is required.",
            },
        ) from exc

    return ParkingApplicationRead.model_validate(application)
