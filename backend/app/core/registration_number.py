import re

REGISTRATION_NUMBER_PATTERN = re.compile(
    r"^[A-Z0-9]{4,10}$",
)


def normalize_registration_number(value: str) -> str:
    return value.strip().upper().replace(" ", "").replace("-", "")


def validate_registration_number(value: str) -> str:
    normalized_value = normalize_registration_number(value)

    if not REGISTRATION_NUMBER_PATTERN.fullmatch(normalized_value):
        raise ValueError("Registration number must contain 4-10 letters or digits.")

    return normalized_value
