import functools
from typing import AsyncGenerator

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from warehouse_service.infra.db.sessionmaker import (
    async_sessionmaker_from_env,
    AsyncSessionmakerProtocol,
)
from warehouse_service.interactors.auth import (
    UserAuthenticateBySessionProtocol,
    UserAuthenticateProtocol,
    UserCreateProtocol,
)
from warehouse_service.interactors.factories.auth import (
    user_authenticate_initialize,
    user_create_initialize,
    session_auth_initialize,
)


@functools.lru_cache(maxsize=1)
def provide_sessionmaker() -> AsyncSessionmakerProtocol:
    return async_sessionmaker_from_env()


async def make_session(
    sessionmaker: AsyncSessionmakerProtocol = Depends(),
) -> AsyncGenerator[AsyncSession, None]:
    try:
        session = sessionmaker.begin()
        yield session
    except Exception:
        await session.rollback()
    finally:
        await session.close()


def provide_user_create(
    session: AsyncSession = Depends(),
) -> UserCreateProtocol:
    return user_create_initialize(sess=session)


def provide_user_authenticate(
    session: AsyncSession = Depends(),
) -> UserAuthenticateProtocol:
    return user_authenticate_initialize(sess=session)


def provide_user_authenticate_by_session(
    session: AsyncSession = Depends(),
) -> UserAuthenticateBySessionProtocol:
    return session_auth_initialize(sess=session)


def set_dependency_injection(app: FastAPI) -> None:
    """
    should rewrite to Dishka
    """
    app.dependency_overrides.update(
        {
            AsyncSessionmakerProtocol: provide_sessionmaker,
            AsyncSession: make_session,
            UserCreateProtocol: provide_user_create,
            UserAuthenticateProtocol: provide_user_authenticate,
            UserAuthenticateBySessionProtocol: provide_user_authenticate_by_session,
        }
    )
