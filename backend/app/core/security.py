from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from jwt.exceptions import InvalidTokenError as PyJWTInvalidTokenError
from pwdlib import PasswordHash

from app.core.config import settings
from app.core.exceptions import InvalidAccessTokenError

_password_haser = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return _password_haser.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _password_haser.verify(plain_password, hashed_password)


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
