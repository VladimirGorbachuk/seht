from uuid import UUID
import datetime

from sqlalchemy import insert, select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from warehouse_service.domain.auth import UserAuth, UserAuthSession, AuthSession


class AuthUserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_login(self, login: str) -> UserAuth | None:
        result = await self.session.execute(select(UserAuth).where(UserAuth.login==login))
        return result.scalar_one_or_none()
    
    async def get_by_session_token(self, session_token: str) -> UserAuthSession | None:
        result = await self.session.execute(select(UserAuthSession).options(joinedload(UserAuthSession.session)).where(AuthSession.session_token==session_token))
        return result.scalar_one_or_none()

    async def create_user_session(self, *, session_token: str, dt_created: datetime.datetime, user_uuid: UUID) -> None:
        await self.session.execute(
            insert(AuthSession).values(
                session_token=session_token,
                user_uuid=user_uuid,
                last_login=dt_created,
            )
        )

    async def add_user(self, *, uuid: UUID, login: str, password_hash: bytes, salt: bytes) -> None:
        return await self.session.execute(
            insert(UserAuth).values(
                uuid=uuid,
                login=login,
                password_hash=password_hash,
                salt=salt,
            ).returning(UserAuth),
        )
