from pwdlib import PasswordHash

_password_haser = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return _password_haser.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _password_haser.verify(plain_password, hashed_password)
