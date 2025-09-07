from dataclasses import dataclass
import datetime
import os
import secrets

from cryptography.exceptions import InvalidKey
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from warehouse_service.entities.auth import PasswordHash, Password, Salt


@dataclass(frozen=True)
class AuthCryptoSettings:
    """
    still need to find better name for it
    """

    SALT_LENGTH: int = 16
    HASH_ITERATIONS: int = 480_000
    HASH_LENGTH: int = 32
    SESSION_ID_HEXADECIMAL_CHARS: int = 16
    SESSION_AUTH_TOKEN_EXPIRATION_SECONDS: float = 6 * 24 * 60 * 60

    @classmethod
    def initialize_from_environment(cls) -> "AuthCryptoSettings":
        return cls(
            SALT_LENGTH=int(os.environ.get("PASSWORD_SALT_LENGTH", 16)),
            HASH_ITERATIONS=int(os.environ.get("PASSWORD_HASH_ITERATIONS", 480_000)),
            HASH_LENGTH=int(os.environ.get("PASSWORD_HASH_LENGTH", 32)),
            SESSION_ID_HEXADECIMAL_CHARS=int(
                os.environ.get("SESSION_ID_HEXADECIMAL_CHARS", 16)
            ),
            SESSION_AUTH_TOKEN_EXPIRATION_SECONDS=float(
                os.environ.get(
                    "SESSION_AUTH_TOKEN_EXPIRATION_SECONDS", 6 * 24 * 60 * 60
                )
            ),
        )


class AuthenticationFailureError(Exception):
    pass


class WrongPasswordError(AuthenticationFailureError):
    pass


class LoginUnknownError(AuthenticationFailureError):
    pass


@dataclass(frozen=True, slots=True)
class PasswordHashAndSalt:
    password_hash: PasswordHash
    salt: Salt


class PasswordHasher:
    def __init__(self, password_hash_settings: AuthCryptoSettings):
        self.settings = password_hash_settings

    def _make_salt(self) -> Salt:
        return Salt(os.urandom(self.settings.SALT_LENGTH))

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
        self,
        *,
        hashed_password_and_salt: PasswordHashAndSalt,
        password: Password,
    ) -> bool:
        kdf = self._make_kdf(hashed_password_and_salt.salt)
        try:
            kdf.verify(password.encode(), hashed_password_and_salt.password_hash)
            return True
        except InvalidKey:
            return False


class AuthTokenController:
    def __init__(self, settings: AuthCryptoSettings):
        self.settings = settings

    def make_hex_token(self) -> str:
        return secrets.token_hex(self.settings.SESSION_ID_HEXADECIMAL_CHARS)

    def check_expired(
        self, dt_now: datetime.datetime, last_login_dt: datetime.datetime
    ) -> bool:
        return (
            last_login_dt
            + datetime.timedelta(
                seconds=self.settings.SESSION_AUTH_TOKEN_EXPIRATION_SECONDS,
            )
            > dt_now
        )
