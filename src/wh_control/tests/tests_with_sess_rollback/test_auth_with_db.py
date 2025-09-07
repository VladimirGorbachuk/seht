from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from testcontainers.postgres import PostgresContainer

from warehouse_service.infra.db.settings import PostgresSettings
from warehouse_service.interactors.auth import (
    UserNotFound,
    UserSessionNotFoundOrExpired,
)
from warehouse_service.dto.auth import UserLoginPwd, UserLoginPwdUUID

from warehouse_service.interactors.factories.auth import (
    user_authenticate_initialize,
    user_create_initialize,
    session_auth_initialize,
)
from warehouse_service.application.auth import AuthCryptoSettings


@pytest.mark.asyncio
async def test_settings_same(
    postgres_settings: PostgresSettings,
    postgres_container_with_migrations: PostgresContainer,
) -> None:
    conn_url = postgres_container_with_migrations.get_connection_url()
    assert conn_url == postgres_settings.full_url


@pytest.mark.asyncio
async def test_interactor_nonexisting_not_found(
    async_session_with_rollback: AsyncSession,
) -> None:
    user_aunthenticate_interactor = user_authenticate_initialize(
        sess=async_session_with_rollback, auth_crypto_settings=AuthCryptoSettings()
    )
    nonexisting = UserLoginPwd(login="testt", password="testt")
    with pytest.raises(UserNotFound):
        await user_aunthenticate_interactor.authenticate_or_deny_user(nonexisting)


@pytest.mark.asyncio
async def test_interactor_user_create(
    async_session_with_rollback: AsyncSession,
) -> None:
    print("WHUTTTT?", async_session_with_rollback)
    user_create_interactor = user_create_initialize(
        sess=async_session_with_rollback, auth_crypto_settings=AuthCryptoSettings()
    )
    user_aunthenticate_interactor = user_authenticate_initialize(
        sess=async_session_with_rollback, auth_crypto_settings=AuthCryptoSettings()
    )
    to_create = UserLoginPwdUUID(login="testt", password="testt", uuid=uuid4())
    to_check = UserLoginPwd(login=to_create.login, password=to_create.password)
    await user_create_interactor.create_user(to_create)
    assert (
        await user_aunthenticate_interactor.authenticate_or_deny_user(to_check)
        is not None
    )


@pytest.mark.asyncio
async def test_interactor_nonexisting_sess_cannot_auth(
    async_session_with_rollback: AsyncSession,
) -> None:
    user_auth_by_session = session_auth_initialize(
        async_session_with_rollback, auth_crypto_settings=AuthCryptoSettings()
    )
    with pytest.raises(UserSessionNotFoundOrExpired):
        await user_auth_by_session.authenticate_or_deny_user("not a real token")


@pytest.mark.asyncio
async def test_interactor_user_create_and_login_and_sess_auth(
    async_session_with_rollback: AsyncSession,
) -> None:
    user_create_interactor = user_create_initialize(
        sess=async_session_with_rollback, auth_crypto_settings=AuthCryptoSettings()
    )
    user_aunthenticate_interactor = user_authenticate_initialize(
        sess=async_session_with_rollback, auth_crypto_settings=AuthCryptoSettings()
    )
    user_auth_by_session = session_auth_initialize(
        async_session_with_rollback, auth_crypto_settings=AuthCryptoSettings()
    )
    to_create = UserLoginPwdUUID(login="testt2", password="testt2", uuid=uuid4())
    to_check = UserLoginPwd(login=to_create.login, password=to_create.password)
    await user_create_interactor.create_user(to_create)
    sess_token = await user_aunthenticate_interactor.authenticate_or_deny_user(to_check)
    assert sess_token is not None
    await user_auth_by_session.authenticate_or_deny_user(sess_token)
