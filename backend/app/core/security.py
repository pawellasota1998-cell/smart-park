from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from typing import Any
from uuid import UUID

import jwt
from jwt.exceptions import InvalidTokenError as PyJWTInvalidTokenError
from pwdlib import PasswordHash

from app.core.config import settings
from app.core.exceptions import InvalidAccessTokenError, InvalidRefreshTokenError


@dataclass(frozen=True)
class RefreshTokenData:
    subject: str
    jti: UUID


_password_haser = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return _password_haser.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _password_haser.verify(plain_password, hashed_password)


def hash_token(token: str) -> str:
    return sha256(token.encode("utf-8")).hexdigest()


def cretae_acces_token(subject: str, expiries_delta: timedelta | None = None) -> str:
    now = datetime.now(UTC)

    if expiries_delta is None:
        expiries_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expieries_at = now + expiries_delta

    payload: dict[str, Any] = {
        "sub": subject,
        "type": "access",
        "iat": now,
        "exp": expieries_at,
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )


def create_refresh_token(*, subject: str, jti: UUID, expires_at: datetime) -> str:
    now = datetime.now(UTC)
    payload: dict[str, Any] = {
        "sub": subject,
        "type": "refresh",
        "jti": str(jti),
        "iat": now,
        "exp": expires_at,
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
    }
    return jwt.encode(
        payload,
        settings.jwt_secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )


def get_acces_token_subject(token: str) -> str:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key.get_secret_value(),
            algorithms=[settings.jwt_algorithm],
            issuer=settings.jwt_issuer,
            audience=settings.jwt_audience,
            options={
                "require": [
                    "sub",
                    "type",
                    "iat",
                    "exp",
                    "iss",
                    "aud",
                ]
            },
        )
    except PyJWTInvalidTokenError as exc:
        raise InvalidAccessTokenError from exc

    subject = payload.get("sub")
    token_type = payload.get("type")

    if not isinstance(subject, str) or not subject:
        raise InvalidAccessTokenError
    if token_type != "access":
        raise InvalidAccessTokenError

    return subject


def get_refresh_token_data(token: str) -> RefreshTokenData:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key.get_secret_value(),
            algorithms=[settings.jwt_algorithm],
            issuer=settings.jwt_issuer,
            audience=settings.jwt_audience,
            options={
                "require": [
                    "sub",
                    "type",
                    "jti",
                    "iat",
                    "exp",
                    "iss",
                    "aud",
                ]
            },
        )
    except PyJWTInvalidTokenError as exc:
        raise InvalidRefreshTokenError from exc

    subject = payload.get("sub")
    token_type = payload.get("type")
    jti_value = payload.get("jti")

    if not isinstance(subject, str) or not subject:
        raise InvalidRefreshTokenError
    if token_type != "refresh":
        raise InvalidRefreshTokenError
    if not isinstance(jti_value, str) or not jti_value:
        raise InvalidRefreshTokenError

    try:
        jti = UUID(jti_value)
    except ValueError as exc:
        raise InvalidRefreshTokenError from exc
    return RefreshTokenData(subject=subject, jti=jti)
