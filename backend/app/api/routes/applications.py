from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.database import get_db
from app.api.dependencies.services import get_application_service
from app.core.exceptions import (
    ParkingApplicationAccessDeniedError,
    ParkingApplicationCannotBeEditedError,
    ParkingApplicationNotFoundError,
)
from app.models.user import User
from app.schemas.application import (
    ParkingApplicationCreate,
    ParkingApplicationRead,
    ParkingApplicationUpdate,
)
from app.services.application_service import ApplicationService

router = APIRouter(
    prefix="/applications",
    tags=["Applications"],
)


@router.post(
    "",
    response_model=ParkingApplicationRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create parking application",
    description="Creates a new parking application for the current user.",
)
def create_application(
    application_data: ParkingApplicationCreate,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    application_service: Annotated[
        ApplicationService,
        Depends(get_application_service),
    ],
) -> ParkingApplicationRead:
    application = application_service.create_application(
        db,
        current_user=current_user,
        application_data=application_data,
    )

    return ParkingApplicationRead.model_validate(application)


@router.get(
    "/me",
    response_model=list[ParkingApplicationRead],
    status_code=status.HTTP_200_OK,
    summary="List my parking applications",
    description="Returns parking applications submitted by the current user.",
)
def list_my_applications(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    application_service: Annotated[
        ApplicationService,
        Depends(get_application_service),
    ],
) -> list[ParkingApplicationRead]:
    applications = application_service.list_my_applications(
        db,
        current_user=current_user,
    )
    return [ParkingApplicationRead.model_validate(application) for application in applications]


@router.get(
    "/{application_id}",
    response_model=ParkingApplicationRead,
    status_code=status.HTTP_200_OK,
    summary="Get my parking application",
    description="Returns a single parking application owned by the current user.",
)
def get_my_application(
    application_id: int,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    application_service: Annotated[
        ApplicationService,
        Depends(get_application_service),
    ],
) -> ParkingApplicationRead:
    try:
        application = application_service.get_my_application(
            db,
            current_user=current_user,
            application_id=application_id,
        )

    except ParkingApplicationNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "PARKING_APPLICATION_NOT_FOUND",
                "message": "Parking application was not found.",
            },
        ) from exc
    except ParkingApplicationAccessDeniedError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "PARKING_APPLICATION_ACCESS_DENIED",
                "message": "You cannot access this parking application.",
            },
        ) from exc

    return ParkingApplicationRead.model_validate(application)


@router.patch(
    "/{application_id}",
    response_model=ParkingApplicationRead,
    status_code=status.HTTP_200_OK,
    summary="Update my parking application",
    description=(
        "Updates a parking application owned by the current user if it is in PENDING or NEEDS_CHANGES status."
    ),
)
def update_my_application(
    application_id: int,
    application_data: ParkingApplicationUpdate,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    application_service: Annotated[
        ApplicationService,
        Depends(get_application_service),
    ],
) -> ParkingApplicationRead:
    try:
        application = application_service.update_my_application(
            db,
            current_user=current_user,
            application_id=application_id,
            application_data=application_data,
        )
    except ParkingApplicationNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "PARKING_APPLICATION_NOT_FOUND",
                "message": "Parking application was not found.",
            },
        ) from exc

    except ParkingApplicationAccessDeniedError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "PARKING_APPLICATION_ACCESS_DENIED",
                "message": "You cannot access this parking application.",
            },
        ) from exc

    except ParkingApplicationCannotBeEditedError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": "PARKING_APPLICATION_CANNOT_BE_EDITED",
                "message": ("Parking application cannot be edited in its current status."),
            },
        ) from exc

    return ParkingApplicationRead.model_validate(application)
