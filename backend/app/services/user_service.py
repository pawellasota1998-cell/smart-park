from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.exceptions import EmailAlreadyExistsError
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def create_user(self, db: Session, user_data: UserCreate) -> User:
        normalized_email = str(user_data.email).strip().lower()
        existing_user = self._repository.get_by_email(db, normalized_email)
        if existing_user is not None:
            raise EmailAlreadyExistsError

        password_hash = hash_password(user_data.password)

        try:
            user = self._repository.create(
                db,
                email=normalized_email,
                password_hash=password_hash,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
            )
            db.commit()
            db.refresh(user)

        except IntegrityError as exc:
            db.rollback()

            existing_user = self._repository.get_by_email(db, normalized_email)
            if existing_user is not None:
                raise EmailAlreadyExistsError from exc
            raise
        except SQLAlchemyError:
            db.rollback()
            raise

        return user
