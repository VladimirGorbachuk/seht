import functools
from typing import AsyncGenerator

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from warehouse_service.infra.db.sessionmaker import PostgresSessions, PostgresSettings
from warehouse_service.interactors.auth import UserCreate, UserAuthenticate
from warehouse_service.serializers.auth import UserLoginPwd, UserLoginPwdUUID


class UserCreateProtocol:
    async def create_user(self, user_login_pwd: UserLoginPwdUUID):
        raise NotImplementedError


class UserAuthenticateProtocol:
    async def authenticate_or_deny_user(self, user_login_pwd: UserLoginPwd) -> bool:
        raise NotImplementedError


@functools.lru_cache(maxsize=1)
def provide_sessionmaker() -> async_sessionmaker:
    settings = PostgresSettings.from_env()
    return PostgresSessions(settings).create_async_sessionmaker()


async def make_session(sessionmaker: async_sessionmaker = Depends()) -> AsyncGenerator[AsyncSession, None]:
    try:
        session = await sessionmaker()
        yield session
    except Exception as e:
        print("should log here", e)
        await session.rollback()
    finally:
        await session.close()


def user_create_inj(session: AsyncSession = Depends()) -> UserCreate:
    return UserCreate(session)


def user_authenticate_inj(session: AsyncSession = Depends()) -> UserAuthenticate:
    return UserAuthenticate(session)



def set_dependency_injection(app: FastAPI):
    """
    should rewrite to Dishka
    """
    app.dependency_overrides.update({
        async_sessionmaker: provide_sessionmaker,
        AsyncSession: make_session,
        UserCreateProtocol: user_create_inj,
        UserAuthenticateProtocol: user_authenticate_inj,
    })