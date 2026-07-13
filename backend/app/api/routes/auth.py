from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.database import get_db
from app.api.dependencies.services import get_auth_service, get_user_service
from app.core.config import settings
from app.core.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    InvalidRefreshTokenError,
)
from app.models.user import User
from app.schemas.auth import RefreshTokenRequest, TokenResponse
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
    description="Creates a new user account with the USER role.",
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
                "message": ("An account with this email already exists."),
            },
        ) from exc
    return UserRead.model_validate(user)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh token pair",
    description=" Rotates a refresh token and returns a new access token and refresh token.",
)
def refresh_token(
    request_data: RefreshTokenRequest,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    auth_service: Annotated[
        AuthService,
        Depends(get_auth_service),
    ],
) -> TokenResponse:
    try:
        token_pair = auth_service.refresh_token_pair(
            db,
            request_data.refresh_token,
        )

    except InvalidRefreshTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "INVALID_REFRESH_TOKEN",
                "message": ("Refresh token is invalid, expired or revoked."),
            },
            headers={
                "WWW-Authenticate": "Bearer",
            },
        ) from exc
    return TokenResponse(
        access_token=token_pair.access_token,
        refresh_token=token_pair.refresh_token,
        expires_in=settings.access_token_expire_minutes * 60,
    )


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Logout user",
    description="Revokes the provided refresh token.",
)
def logout_user(
    request_data: RefreshTokenRequest,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    auth_service: Annotated[
        AuthService,
        Depends(get_auth_service),
    ],
) -> Response:
    try:
        auth_service.revoke_refresh_token(
            db,
            request_data.refresh_token,
        )

    except InvalidRefreshTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "INVALID_REFRESH_TOKEN",
                "message": ("Refresh token is invalid, expired or revoked."),
            },
            headers={
                "WWW-Authenticate": "Bearer",
            },
        ) from exc

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )


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
        user = auth_service.authenticate_user(db, email=form_data.username, password=form_data.password)
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

    token_pair = auth_service.issue_token_pair(
        db,
        user,
    )

    return TokenResponse(
        access_token=token_pair.access_token,
        refresh_token=token_pair.refresh_token,
        expires_in=settings.access_token_expire_minutes * 60,
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
