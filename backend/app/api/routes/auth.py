from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.database import get_db
from app.api.dependencies.services import get_auth_service, get_user_service
from app.core.config import settings
from app.core.exceptions import EmailAlreadyExistsError, InvalidCredentialsError
from app.models.user import User
from app.schemas.auth import TokenResponse
from app.schemas.user import UserCreate, UserRead
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter(
    prefix="/auth",  # Każdy endpoint z tego routera zaczyna się od /health
    tags=["Authentication"],  # grupowanie endpointów w dokumentacji api
)


@router.post(
    "/register",
    # Odpowiedź HTTP ma być zgodna ze schematem HealthResponse
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
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
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": "EMAIL_ALREADY_EXISTS",
                "message": ("An account with this email " "already exists."),
            },
        ) from exc
    return UserRead.model_validate(user)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Login user",
    description=" Authenticated a user and returns a JQT acces token",
)
def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)],
    db: Annotated[Session, Depends(get_db)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> TokenResponse:
    try:
        user = auth_service.authenticate_user(
            db, email=form_data.username, password=form_data.password
        )
    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "INVALID_CREDENTIALS",
                "message": "Invalid email or password.",
            },
            headers={
                "WWW-Authenticate": "Bearer",
            },
        ) from exc

    access_token = auth_service.issue_acces_token(user)

    return TokenResponse(
        access_token=access_token, expires_in=settings.access_token_expire_minutes * 60
    )


@router.get(
    "/me",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Get current userr",
    description="Returns the currently authenticated user.",
)
def get_me(current_user: Annotated[User, Depends(get_current_user)]) -> UserRead:
    return UserRead.model_validate(current_user)
