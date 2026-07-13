from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.api.dependencies.auth import get_current_user
from app.models.enums import UserRole
from app.models.user import User

SUPERVISOR_ROLES = {
    UserRole.SUPERVISOR,
    UserRole.ADMIN,
}


def require_supervisor(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
) -> User:
    if current_user.role not in SUPERVISOR_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "INSUFFICIENT_PERMISSIONS",
                "message": "Supervisor permissions are required.",
            },
        )

    return current_user
