from unittest.mock import Mock, patch

from sqlalchemy.orm import Session

from app.models.enums import UserRole
from app.models.user import User
from app.repositories.user_repository import (
    UserRepository,
)
from app.schemas.user import UserCreate
from app.services.user_service import UserService


def test_create_user_hashes_password_and_commits() -> None:
    db = Mock(spec=Session)
    repository = Mock(spec=UserRepository)
    repository.get_by_email.return_value = None

    created_user = User(
        id=1,
        email="pawel@example.com",
        password_hash="hashed-password",
        first_name="Paweł",
        last_name="Lasota",
        role=UserRole.USER,
    )

    repository.create.return_value = created_user

    service = UserService(repository=repository)

    user_data = UserCreate(
        email="Pawel@Example.com",
        password="StrongPassword123!",
        first_name="Paweł",
        last_name="Lasota",
    )
    with patch(
        "app.services.user_service.hash_password",
        return_value="hashed-password",
    ) as hash_password_mock:
        result = service.create_user(
            db,
            user_data,
        )

    assert result is created_user

    hash_password_mock.assert_called_once_with("StrongPassword123!")

    repository.create.assert_called_once_with(
        db,
        email="pawel@example.com",
        password_hash="hashed-password",
        first_name="Paweł",
        last_name="Lasota",
    )

    db.refresh.assert_called_once_with(created_user)

    db.commit.assert_called_once()
