class EmailAlreadyExistsError(Exception):
    """Raised when registration uses an existing email address."""


class InvalidCredentialsError(Exception):
    """Raised when login credentials are invalid."""


class InvalidAccessTokenError(Exception):
    """Raised when an access token is invalid or expired."""
