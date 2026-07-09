from enum import StrEnum


class UserRole(StrEnum):
    USER = "USER"
    SUPERVISOR = "SUPERVISOR"
    ADMIN = "ADMIN"


class ApplicationStatus(StrEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    NEEDS_CHANGES = "NEEDS_CHANGES"
