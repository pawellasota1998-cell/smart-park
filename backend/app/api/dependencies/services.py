from app.repositories.application_repository import (
    ParkingApplicationRepository,
)
from app.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)
from app.repositories.user_repository import UserRepository
from app.services.application_service import ApplicationService
from app.services.auth_service import AuthService
from app.services.barrier_service import BarrierService
from app.services.user_service import UserService

_user_repository = UserRepository()
_refresh_token_repository = RefreshTokenRepository()
_application_repository = ParkingApplicationRepository()

_barrier_service = BarrierService(
    application_repository=_application_repository,
)
_user_service = UserService(repository=_user_repository)
_auth_service = AuthService(user_repository=_user_repository, refresh_token_repository=_refresh_token_repository)
_application_service = ApplicationService(repository=_application_repository)


def get_user_service() -> UserService:
    return _user_service


def get_auth_service() -> AuthService:
    return _auth_service


def get_application_service() -> ApplicationService:
    return _application_service


def get_barrier_service() -> BarrierService:
    return _barrier_service
