import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from warehouse_service.interactors.auth import (
    UserAuthenticate,
    UserCreate,
    UserAuthenticateBySession,
)
from warehouse_service.repository.auth_user import AuthUserRepo
from warehouse_service.application.auth import (
    PasswordHasher,
    AuthCryptoSettings,
    AuthTokenController,
)


def user_authenticate_initialize(
    sess: AsyncSession, auth_crypto_settings: AuthCryptoSettings
) -> UserAuthenticate:
    hasher = PasswordHasher(auth_crypto_settings)
    auth_token_controller = AuthTokenController(auth_crypto_settings)
    auth_repo = AuthUserRepo(sess)
    return UserAuthenticate(
        password_hasher=hasher,
        auth_user_repo=auth_repo,
        auth_token_controller=auth_token_controller,
        dt_now=datetime.datetime.now(),
    )


def user_create_initialize(
    sess: AsyncSession, auth_crypto_settings: AuthCryptoSettings
) -> UserCreate:
    hasher = PasswordHasher(auth_crypto_settings)
    auth_repo = AuthUserRepo(sess)
    return UserCreate(
        password_hasher=hasher,
        auth_user_repo=auth_repo,
    )


def session_auth_initialize(
    sess: AsyncSession, auth_crypto_settings: AuthCryptoSettings
) -> UserAuthenticateBySession:
    auth_repo = AuthUserRepo(sess)
    auth_token_controller = AuthTokenController(auth_crypto_settings)
    return UserAuthenticateBySession(
        auth_user_repo=auth_repo,
        dt_now=datetime.datetime.now(),
        auth_token_controller=auth_token_controller,
    )
