from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.schemas.health import HealthResponse, ReadinessResponse
from app.services.health_service import check_database_connection

router = APIRouter(
    prefix="/health",  # Każdy endpoint z tego routera zaczyna się od /health
    tags=["health"],  # grupowanie endpointów w dokumentacji api
)


@router.get(
    "",
    # Odpowiedź HTTP ma być zgodna ze schematem HealthResponse
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Check API health",
    description="Checks whether the  Euro Park API is running",
)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok", service="euro-park-api", version="0.1.0")


@router.get(
    "/ready",
    # Odpowiedź HTTP ma być zgodna ze schematem HealthResponse
    response_model=ReadinessResponse,
    status_code=status.HTTP_200_OK,
    summary="Check API readiness",
    description="Checks whether the API can connect to the database.",
)
def readindess_check(db: Annotated[Session, Depends(get_db)]) -> ReadinessResponse:
    try:
        check_database_connection(db)
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "code": "DATABASE_UNAVAILABLE",
                "message": "Database connection is unavailable",
            },
        ) from exc

    return ReadinessResponse(status="ok", database="mssql")
