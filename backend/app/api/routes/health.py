from fastapi import APIRouter, status

from app.schemas.health import HealthResponse

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
