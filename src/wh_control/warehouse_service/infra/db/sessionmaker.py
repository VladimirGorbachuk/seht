from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker

from warehouse_service.infra.db.settings import PostgresSettings


class PostgresSessions:
    def __init__(self, settings: PostgresSettings):
        self.settings = settings
            
    def create_async_sessionmaker(self) -> async_sessionmaker:
        engine = create_async_engine(
            self.settings.full_url,
            echo=True,
            pool_size=10,
            max_overflow=15,
            connect_args={"connect_timeout": 5, "statement_timeout": 30},
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
            connect_args={"connect_timeout": 50, "statement_timeout": 300},
        )
        return sessionmaker(engine, autoflush=False, expire_on_commit=False)