from sqlalchemy.orm import Session

from app.core.exceptions import InvalidAccessTokenError, InvalidCredentialsError
from app.core.security import (
    cretae_acces_token,
    get_acces_token_subject,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def authenticate_user(self, db: Session, *, email: str, password: str):
        normalize_email = email.strip().lower()

        user = self._repository.get_by_email(db, normalize_email)

        if user is None:
            raise InvalidCredentialsError
        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError
        if not user.is_active:
            raise InvalidCredentialsError
        return user

    def issue_acces_token(self, user: User) -> str:
        return cretae_acces_token(subject=str(user.id))

    def get_user_from_acces_token(self, db: Session, token: str) -> User:
        subject = get_acces_token_subject(token)

        try:
            user_id = int(subject)
        except ValueError as exc:
            raise InvalidAccessTokenError from exc

        user = self._repository.get_by_id(db, user_id)

        if user is None:
            raise InvalidAccessTokenError
        if not user.is_active:
            raise InvalidAccessTokenError
        return user
