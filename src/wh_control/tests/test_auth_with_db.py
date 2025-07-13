import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from testcontainers.postgres import PostgresContainer

from warehouse_service.infra.db.settings import PostgresSettings
from warehouse_service.interactors.auth import UserAuthenticate
from warehouse_service.serializers.auth import UserLoginPwd



@pytest.mark.asyncio
async def test_fromscratch(
        async_session_with_rollback: AsyncSession,
        postgres_container: PostgresContainer,
    ):
    conn_url = postgres_container.get_connection_url()
    engine = create_async_engine(
            conn_url,
            echo=True,
            pool_size=10,
            max_overflow=15,
            connect_args={"connect_timeout": 5},
        )
    sessmaker = async_sessionmaker(
            engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
        )
    sess = sessmaker()
    assert await sess.begin()
    assert await sess.connection()
    assert await sess.close()  




@pytest.mark.asyncio
async def test_settings_same(
        postgres_settings: PostgresSettings,
        postgres_container: PostgresContainer,
    ):
    conn_url = postgres_container.get_connection_url()
    assert conn_url == postgres_settings.full_url




@pytest.mark.asyncio
async def test_sess(
        async_session_with_rollback: AsyncSession,
        postgres_container: PostgresContainer,
    ):
    assert await async_session_with_rollback.begin()
    assert await async_session_with_rollback.connection()
    assert await async_session_with_rollback.close()  



@pytest.mark.asyncio
async def test_interactor(
        user_authenticate_interactor_with_rollback: UserAuthenticate,
        postgres_container: PostgresContainer,
    ):
    nonexisting = UserLoginPwd(login="testt", password="testt")
    assert await user_authenticate_interactor_with_rollback.authenticate_or_deny_user(nonexisting) is False
