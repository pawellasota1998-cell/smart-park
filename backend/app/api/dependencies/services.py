from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.user_service import UserService

_user_repository = UserRepository()

_user_service = UserService(repository=_user_repository)
_auth_service = AuthService(repository=_user_repository)


def get_user_service() -> UserService:
    return _user_service


def get_auth_service() -> AuthService:
    return _auth_service
