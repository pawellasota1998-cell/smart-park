from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.status import HTTP_409_CONFLICT

from app.api.dependencies.database import get_db
from app.api.dependencies.services import get_user_service
from app.core.exceptions import EmailAlreadyExistsError
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter(
    prefix="/auth",  # Każdy endpoint z tego routera zaczyna się od /health
    tags=["Authentication"],  # grupowanie endpointów w dokumentacji api
)


@router.post(
    "/register",
    # Odpowiedź HTTP ma być zgodna ze schematem HealthResponse
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Register user",
    description="Creates a new user account " "with the USER role.",
)
def register(
    user_data: UserCreate,
    db: Annotated[Session, Depends(get_db)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserRead:
    try:
        user = user_service.create_user(db, user_data)
    except EmailAlreadyExistsError as exc:

        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail={
                "code": "EMAIL_ALREADY_EXISTS",
                "message": ("An account with this email " "already exists."),
            },
        ) from exc
    return UserRead.model_validate(user)
