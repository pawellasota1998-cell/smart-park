from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import UserRole
from app.models.user import User


class UserRepository:
    def get_by_id(
        self,
        db: Session,
        user_id: int,
    ) -> User | None:
        return db.get(User, user_id)

    def get_by_email(self, db: Session, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return db.scalar(statement)

    def create(
        self,
        db: Session,
        *,
        email: str,
        password_hash: str,
        first_name: str,
        last_name: str,
    ) -> User:
        user = User(
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            role=UserRole.USER,
        )
        db.add(user)
        db.flush()
        return user
