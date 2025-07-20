import asyncio
import os
import sys
from typing import Generator
from urllib.parse import urlparse

import alembic.config
from sqlalchemy.ext.asyncio import AsyncSession
from testcontainers.postgres import PostgresContainer
import alembic
import pytest

from warehouse_service.factories.auth_interactors import user_authenticate_from_session, user_create_from_session, session_auth_from_session
from warehouse_service.infra.db.migrations import ALEMBIC_INI_LOCATION, ALEMBIC_SCRIPT_LOCATION
from warehouse_service.infra.db.sessionmaker import PostgresSessions
from warehouse_service.infra.db.settings import PostgresSettings
from warehouse_service.application.auth import AuthCryptoSettings
from warehouse_service.interactors.auth import UserAuthenticate, UserCreate, UserAuthenticateBySession
from warehouse_service.repository.auth_user import AuthUserRepo


@pytest.fixture(scope="session", autouse=True)
def event_loop_policy():
    if sys.platform == "win32":
        yield asyncio.WindowsSelectorEventLoopPolicy()


@pytest.fixture()
def postgres_container() -> Generator[PostgresContainer, None, None]:
    postgres = PostgresContainer(
        "postgres:16", 
        driver="psycopg",
    )
    try:
        p = postgres.start()
        yield p
    finally:
        postgres.stop()




@pytest.fixture()
def postgres_container_with_migrations(postgres_container: PostgresContainer) -> Generator[PostgresContainer, None, None]:
    alembic_config = alembic.config.Config(file_=os.path.join(ALEMBIC_INI_LOCATION, "alembic.ini"))
    alembic_config.set_main_option("script_location", ALEMBIC_SCRIPT_LOCATION)
    alembic_config.attributes["connection"] = postgres_container.get_connection_url()
    alembic_config.set_main_option(
        "sqlalchemy.url",
        postgres_container.get_connection_url()
    )
    assert alembic_config.get_main_option("sqlalchemy.url") == postgres_container.get_connection_url()
    assert alembic_config.get_section(alembic_config.config_ini_section, {})["sqlalchemy.url"] == postgres_container.get_connection_url()
    alembic.command.upgrade(config=alembic_config, revision="head")
    yield postgres_container



@pytest.fixture()
def postgres_settings(postgres_container_with_migrations: PostgresContainer) -> Generator[PostgresSettings, None, None]:
    port = urlparse(postgres_container_with_migrations.get_connection_url()).port
    yield PostgresSettings(
        user=postgres_container_with_migrations.username,
        password=postgres_container_with_migrations.password,
        host=postgres_container_with_migrations.get_container_host_ip(),
        port=port, 
        db=postgres_container_with_migrations.dbname,
    )



@pytest.fixture()
def async_session_with_rollback(postgres_settings: PostgresSettings) -> Generator[AsyncSession, None, None]:
    session_maker = PostgresSessions(postgres_settings).create_async_sessionmaker()
    try:
        session = session_maker()
        yield session
    finally:
        session.rollback()



@pytest.fixture()
def auth_repo_with_rollback(async_session_with_rollback: AsyncSession) -> Generator[AuthUserRepo, None, None]:
    yield AuthUserRepo(session=async_session_with_rollback)



@pytest.fixture()
def user_authenticate_interactor_with_rollback(
    async_session_with_rollback: AsyncSession,
) -> Generator[UserAuthenticate, None, None]:
    yield user_authenticate_from_session(sess=async_session_with_rollback, auth_crypto_settings=AuthCryptoSettings())


@pytest.fixture()
def user_create_interactor_with_rollback(
    async_session_with_rollback: AsyncSession,
) -> Generator[UserCreate, None, None]:
    yield user_create_from_session(sess=async_session_with_rollback, auth_crypto_settings=AuthCryptoSettings())


@pytest.fixture()
def user_authenticate_by_session_with_rollback(
    async_session_with_rollback: AsyncSession,
) -> Generator[UserAuthenticateBySession, None, None]:
    yield session_auth_from_session(sess=async_session_with_rollback)
