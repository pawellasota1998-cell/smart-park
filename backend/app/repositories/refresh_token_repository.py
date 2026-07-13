from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:
    def get_by_jti(self, db: Session, jti: UUID) -> RefreshToken | None:
        statement = select(RefreshToken).where(RefreshToken.jti == jti)
        return db.scalar(statement)

    def create(
        self, db: Session, user_id: int, jti: UUID, token_hash: str, expires_at
    ) -> RefreshToken:
        refresh_token = RefreshToken(
            user_id=user_id, jti=jti, token_hash=token_hash, expires_at=expires_at
        )
        db.add(refresh_token)
        db.flush()
        return refresh_token

    def revoke(
        self, db: Session, refresh_token: RefreshToken, *, revoked_at: datetime
    ) -> None:
        refresh_token.revoked_at = revoked_at
        db.flush()
