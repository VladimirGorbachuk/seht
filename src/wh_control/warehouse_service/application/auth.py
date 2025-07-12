from dataclasses import dataclass
import os
from typing import NewType

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


Password = NewType("Password", str)
Salt = NewType("Salt", bytes)
PasswordHash = NewType("PasswordHash", bytes)
WebsocketTicker = NewType("WebsocketTicker", str)


@dataclass(frozen=True)
class PasswordHashSettings:
    SALT_LENGTH: int = 16
    HASH_ITERATIONS: int = 480_000
    HASH_LENGTH: int = 32

    @classmethod
    def initialize_from_environment(cls) -> "PasswordHashSettings":
        return cls(
            SALT_LENGTH=os.environ.get("PASSWORD_SALT_LENGTH", 16),
            HASH_ITERATIONS=os.environ.get("PASSWORD_HASH_ITERATIONS", 480_000),
            HASH_LENGTH=os.environ.get("PASSWORD_HASH_LENGTH", 32),
        )



class AuthenticationFailureError(Exception):
    pass


class WrongPasswordError(AuthenticationFailureError):
    pass


class LoginUnknownError(AuthenticationFailureError):
    pass


@dataclass(frozen=True, slots=True)
class PasswordHashAndSalt:
    password_hash: bytes
    salt: bytes


class PasswordHasher:
    def __init__(self, password_hash_settings: PasswordHashSettings):
        self.settings = password_hash_settings

    def _make_salt(self) -> Salt:
        return os.urandom(self.settings.SALT_LENGTH)

    def _make_kdf(self, salt: Salt) -> PBKDF2HMAC:
        return PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.settings.HASH_LENGTH,
            salt=salt,
            iterations=self.settings.HASH_ITERATIONS,
        )

    def hash_password(self, password: Password) -> PasswordHashAndSalt:
        salt = self._make_salt()
        kdf = self._make_kdf(salt)
        password_hash = kdf.derive(password.encode())
        return PasswordHashAndSalt(password_hash=password_hash, salt=salt)

    def verify_password_hash(
        self, *, hashed_password_and_salt: PasswordHashAndSalt, password: Password,
    ) -> bool:
        kdf = self._make_kdf(hashed_password_and_salt.salt)
        return kdf.verify(password.encode(), hashed_password_and_salt.password_hash)


