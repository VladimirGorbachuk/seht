from uuid import UUID

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from warehouse_service.domain.auth import UserAuth


class AuthUserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_login(self, login: str) -> UserAuth | None:
        result = await self.session.execute(select(UserAuth).where(UserAuth.login==login))
        return result.scalar_one_or_none()
    
    async def add_user(self, uuid: UUID, login: str, password_hash: bytes, salt: bytes) -> None:
        return await self.session.execute(
            insert(UserAuth).values(
                uuid=uuid,
                login=login,
                password_hash=password_hash,
                salt=salt,
            ).returning(UserAuth),
        )
