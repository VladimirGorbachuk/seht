import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from testcontainers.postgres import PostgresContainer

from warehouse_service.infra.db.settings import PostgresSettings
from warehouse_service.interactors.auth import UserAuthenticate, UserNotFound
from warehouse_service.serializers.auth import UserLoginPwd


@pytest.mark.asyncio
async def test_settings_same(
        postgres_settings: PostgresSettings,
        postgres_container_with_migrations: PostgresContainer,
    ):
    conn_url = postgres_container_with_migrations.get_connection_url()
    assert conn_url == postgres_settings.full_url



@pytest.mark.asyncio
async def test_interactor_nonexisting_not_found(
        async_session_with_rollback: AsyncSession,
        user_authenticate_interactor_with_rollback: UserAuthenticate,
    ):
    assert await async_session_with_rollback.begin()
    nonexisting = UserLoginPwd(login="testt", password="testt")
    with pytest.raises(UserNotFound):
        await user_authenticate_interactor_with_rollback.authenticate_or_deny_user(nonexisting)
