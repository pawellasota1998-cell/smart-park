from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.dependencies.services import get_barrier_service
from app.schemas.barrier import BarrierAccessRequest, BarrierAccessResponse
from app.services.barrier_service import BarrierService

router = APIRouter(
    prefix="/barrier",
    tags=["Barrier"],
)


@router.post(
    "/check-access",
    response_model=BarrierAccessResponse,
    status_code=status.HTTP_200_OK,
    summary="Check vehicle access",
    description=("Checks whether a vehicle has access based on " "an approved parking application."),
)
def check_access(
    request_data: BarrierAccessRequest,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    barrier_service: Annotated[
        BarrierService,
        Depends(get_barrier_service),
    ],
) -> BarrierAccessResponse:
    result = barrier_service.check_access(
        db,
        request_data=request_data,
    )
    return BarrierAccessResponse(
        registration_number=result.registration_number,
        access_granted=result.access_granted,
    )
