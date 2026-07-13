class EmailAlreadyExistsError(Exception):
    """Raised when registration uses an existing email address."""


class InvalidCredentialsError(Exception):
    """Raised when login credentials are invalid."""


class InvalidAccessTokenError(Exception):
    """Raised when an access token is invalid or expired."""


class InvalidRefreshTokenError(Exception):
    """Raised when a refresh token is invalid, expired or revoked."""


class ParkingApplicationNotFoundError(Exception):
    """Raised when a parking application cannot be found."""


class ParkingApplicationAccessDeniedError(Exception):
    """Raised when a user tries to access someone else's application."""


class ParkingApplicationCannotBeEditedError(Exception):
    """Raised when an application cannot be edited in its current status."""


class ParkingApplicationCannotBeReviewedError(Exception):
    """Raised when an application cannot be reviewed in its current status."""


class SupervisorCommentRequiredError(Exception):
    """Raised when supervisor comment is required but missing."""
