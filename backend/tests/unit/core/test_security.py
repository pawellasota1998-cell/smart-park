from app.core.security import (
    hash_password,
    verify_password,
)


def test_password_hash_can_be_verified() -> None:
    plain_password = "StrongPassword123!"

    hashed_password = hash_password(plain_password)

    assert hashed_password != plain_password
    assert verify_password(
        plain_password,
        hashed_password,
    )
    assert not verify_password(
        "WrongPassword123!",
        hashed_password,
    )
