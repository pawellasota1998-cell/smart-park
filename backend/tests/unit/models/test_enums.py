from app.models.enums import ApplicationStatus, UserRole


def test_user_roles_are_defined() -> None:
    assert {role.value for role in UserRole} == {
        "USER",
        "SUPERVISOR",
        "ADMIN",
    }


def test_application_statuses_are_defined() -> None:
    assert {status.value for status in ApplicationStatus} == {
        "PENDING",
        "APPROVED",
        "REJECTED",
        "NEEDS_CHANGES",
    }
