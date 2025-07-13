import asyncio
import sys
from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession
from testcontainers.postgres import PostgresContainer
import pytest

from warehouse_service.infra.db.sessionmaker import PostgresSessions
from warehouse_service.infra.db.settings import PostgresSettings
from warehouse_service.application.auth import PasswordHasher, PasswordHashSettings
from warehouse_service.interactors.auth import UserAuthenticate
from warehouse_service.repository.auth_user import AuthUserRepo


@pytest.fixture(scope="session", autouse=True)
def event_loop_policy():
    if sys.platform == "win32":
        yield asyncio.WindowsSelectorEventLoopPolicy()


@pytest.fixture
def password_hasher() -> Generator[PasswordHasher, None, None]:
    settings = PasswordHashSettings.initialize_from_environment()
    yield PasswordHasher(settings)


@pytest.fixture()
def postgres_settings() -> Generator[PostgresSettings, None, None]:
    yield PostgresSettings("testuser", "testpwd", "testhost", 5432, "testdb")


@pytest.fixture()
def async_session_with_rollback(postgres_settings: PostgresSettings) -> Generator[AsyncSession, None, None]:
    session_maker = PostgresSessions(postgres_settings).create_async_sessionmaker()
    try:
        session = session_maker()
        yield session
    finally:
        session.rollback()


@pytest.fixture()
def postgres_container(postgres_settings: PostgresSettings) -> Generator[PostgresContainer, None, None]:
    with PostgresContainer(
        "postgres:16", 
        port=postgres_settings.port,
        username=postgres_settings.user,
        password=postgres_settings.password,
        dbname=postgres_settings.db,
        driver="psycopg",
    ) as postgres:
        yield postgres



@pytest.fixture()
def auth_repo_with_rollback(async_session_with_rollback: AsyncSession) -> Generator[AuthUserRepo, None, None]:
    yield AuthUserRepo(session=async_session_with_rollback)


@pytest.fixture()
def user_authenticate_interactor_with_rollback(
    auth_repo_with_rollback: AuthUserRepo,
    password_hasher: PasswordHasher,
) -> Generator[UserAuthenticate, None, None]:
    yield UserAuthenticate(password_hasher=password_hasher, auth_user_repo=auth_repo_with_rollback)