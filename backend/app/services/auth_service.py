from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import (
    InvalidAccessTokenError,
    InvalidCredentialsError,
    InvalidRefreshTokenError,
)
from app.core.security import (
    create_refresh_token,
    cretae_acces_token,
    get_acces_token_subject,
    get_refresh_token_data,
    hash_token,
    verify_password,
)
from app.models.user import User
from app.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)
from app.repositories.user_repository import UserRepository


@dataclass(frozen=True)
class TokenPair:
    access_token: str
    refresh_token: str


def utc_now_naive() -> datetime:
    return datetime.now(
        UTC,
    ).replace(
        tzinfo=None,
    )


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        refresh_token_repository: RefreshTokenRepository,
    ) -> None:
        self._user_repository = user_repository
        self._refresh_token_repository = refresh_token_repository

    def _create_refresh_token(self, db: Session, user: User):
        jti = uuid4()

        expires_at_aware = datetime.now(UTC) + timedelta(
            days=settings.refresh_token_expire_days
        )

        refresh_token = create_refresh_token(
            subject=str(user.id),
            jti=jti,
            expires_at=expires_at_aware,
        )

        self._refresh_token_repository.create(
            db,
            user_id=user.id,
            jti=jti,
            token_hash=hash_token(refresh_token),
            expires_at=expires_at_aware.replace(
                tzinfo=None,
            ),
        )

        return refresh_token

    def authenticate_user(self, db: Session, *, email: str, password: str):
        normalize_email = email.strip().lower()

        user = self._user_repository.get_by_email(db, normalize_email)

        if user is None:
            raise InvalidCredentialsError
        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError
        if not user.is_active:
            raise InvalidCredentialsError
        return user

    def issue_acces_token(self, user: User) -> str:
        return cretae_acces_token(subject=str(user.id))

    def issue_token_pair(self, db: Session, user: User) -> TokenPair:
        try:
            access_token = self.issue_acces_token(user)
            refresh_token = self._create_refresh_token(
                db,
                user,
            )
            db.commit()

        except SQLAlchemyError:
            db.rollback()
            raise
        return TokenPair(access_token=access_token, refresh_token=refresh_token)

    def refresh_token_pair(self, db: Session, refresh_token: str) -> TokenPair:
        token_data = get_refresh_token_data(refresh_token)
        token_hash = hash_token(refresh_token)
        stored_refresh_token = self._refresh_token_repository.get_by_jti(
            db, token_data.jti
        )

        if stored_refresh_token is None:
            raise InvalidRefreshTokenError
        if stored_refresh_token.token_hash != token_hash:
            raise InvalidRefreshTokenError
        if stored_refresh_token.revoked_at is not None:
            raise InvalidRefreshTokenError

        if stored_refresh_token.expires_at <= utc_now_naive():
            raise InvalidRefreshTokenError

        try:
            user_id = int(token_data.subject)
        except ValueError as exc:
            raise InvalidRefreshTokenError from exc

        user = self._user_repository.get_by_id(db, user_id)

        if user is None:
            raise InvalidRefreshTokenError

        if not user.is_active:
            raise InvalidRefreshTokenError

        try:
            self._refresh_token_repository.revoke(
                db, stored_refresh_token, revoked_at=utc_now_naive()
            )

            new_access_token = self.issue_acces_token(user)

            new_refresh_token = self._create_refresh_token(
                db,
                user,
            )
            db.commit()

        except SQLAlchemyError:
            db.rollback()
            raise
        return TokenPair(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
        )

    def revoke_refresh_token(self, db: Session, refresh_token: str) -> None:
        token_data = get_refresh_token_data(refresh_token)

        token_hash = hash_token(
            refresh_token,
        )

        stored_refresh_token = self._refresh_token_repository.get_by_jti(
            db, token_data.jti
        )

        if stored_refresh_token is None:
            raise InvalidRefreshTokenError

        if stored_refresh_token.token_hash != token_hash:
            raise InvalidRefreshTokenError

        if stored_refresh_token.revoked_at is not None:
            raise InvalidRefreshTokenError

        try:
            self._refresh_token_repository.revoke(
                db,
                stored_refresh_token,
                revoked_at=utc_now_naive(),
            )

            db.commit()

        except SQLAlchemyError:
            db.rollback()
            raise

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
