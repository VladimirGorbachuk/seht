from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from infra.db.user import AuthUser


class AuthUserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_login(self, login: str) -> AuthUser | None:
        return await self.session.execute(select(AuthUser).where(AuthUser.login==login))
    
    async def add_user(self, login: str, password_hash: str, salt: str) -> None:
        return await self.session.execute(insert(AuthUser(login=login, password_hash=password_hash, salt=salt)))
