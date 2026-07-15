from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.enums import UserRole
from app.models.user import User

DEMO_USERS = [
    {
        "email": "user@example.com",
        "password": "Password123!",
        "first_name": "Demo_user",
        "last_name": "User",
        "role": UserRole.USER,
    },
    {
        "email": "supervisor@example.com",
        "password": "Password123!",
        "first_name": "Demo_supervisor",
        "last_name": "Supervisor",
        "role": UserRole.SUPERVISOR,
    },
]


def seed_demo_users() -> None:
    with SessionLocal() as db:
        for user_data in DEMO_USERS:
            existing_user = db.scalar(
                select(User).where(
                    User.email == user_data["email"],
                )
            )

            if existing_user is not None:
                existing_user.role = user_data["role"]
                existing_user.is_active = True
                continue

            user = User(
                email=user_data["email"],
                password_hash=hash_password(user_data["password"]),
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                role=user_data["role"],
                is_active=True,
            )

            db.add(user)

        db.commit()


if __name__ == "__main__":
    seed_demo_users()
    print("Demo users created or updated.")
