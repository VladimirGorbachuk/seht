from typing import Protocol

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker

from warehouse_service.infra.db.settings import PostgresSettings


class AsyncSessionmakerProtocol(Protocol):
    def __call__(self) -> AsyncSession:
        pass


class PostgresSessions:
    def __init__(self, settings: PostgresSettings):
        self.settings = settings

    def create_async_sessionmaker(self) -> AsyncSessionmakerProtocol:
        engine = create_async_engine(
            self.settings.full_url,
            echo=True,
            pool_size=10,
            max_overflow=15,
            connect_args={
                "connect_timeout": 5,
                "options": "-c statement_timeout=10000",
            },
        )
        return async_sessionmaker(
            engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
        )

    def create_sync_sessionmaker(self) -> sessionmaker:
        engine = create_engine(
            self.settings.full_url,
            echo=True,
            pool_size=10,
            max_overflow=15,
            connect_args={
                "connect_timeout": 5,
                "options": "-c statement_timeout=100000",
            },
        )
        return sessionmaker(engine, autoflush=False, expire_on_commit=False)


def async_sessionmaker_from_env() -> AsyncSessionmakerProtocol:
    settings = PostgresSettings.from_env()
    return PostgresSessions(settings).create_async_sessionmaker()
