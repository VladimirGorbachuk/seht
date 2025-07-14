from uuid import UUID

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from warehouse_service.infra.db.user import AuthUser


class AuthUserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_login(self, login: str) -> AuthUser | None:
        result = await self.session.execute(select(AuthUser).where(AuthUser.login==login))
        return result.scalar_one_or_none()
    
    async def add_user(self, uuid: UUID, login: str, password_hash: bytes, salt: bytes) -> None:
        return await self.session.execute(insert(AuthUser).values(uuid=uuid, login=login, password_hash=password_hash, salt=salt).returning(AuthUser))
