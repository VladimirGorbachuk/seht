import datetime

from warehouse_service.application.auth import (
    PasswordHashAndSalt,
    PasswordHasher,
    AuthTokenController,
)
from warehouse_service.domain.auth import UserAuthSession
from warehouse_service.dto.auth import UserLoginPwd, UserLoginPwdUUID
from warehouse_service.repository.auth_user import AuthUserRepo


class UserNotFound(Exception):
    pass


class UserSessionNotFoundOrExpired(Exception):
    pass


class UserCreate:
    def __init__(
        self, *, password_hasher: PasswordHasher, auth_user_repo: AuthUserRepo
    ):
        self.password_hasher = password_hasher
        self.auth_user_repo = auth_user_repo

    async def create_user(self, user_login_pwd: UserLoginPwdUUID):
        password_salt_and_hash = self.password_hasher.hash_password(
            user_login_pwd.password
        )
        await self.auth_user_repo.add_user(
            uuid=user_login_pwd.uuid,
            login=user_login_pwd.login,
            salt=password_salt_and_hash.salt,
            password_hash=password_salt_and_hash.password_hash,
        )


class UserAuthenticate:
    def __init__(
        self,
        *,
        password_hasher: PasswordHasher,
        auth_user_repo: AuthUserRepo,
        auth_token_controller: AuthTokenController,
        dt_now: datetime.datetime,
    ):
        self.password_hasher = password_hasher
        self.auth_user_repo = auth_user_repo
        self.auth_token_controller = auth_token_controller
        self.dt_now = dt_now

    async def authenticate_or_deny_user(self, user_login_pwd: UserLoginPwd) -> str:
        user_or_none = await self.auth_user_repo.get_by_login(
            login=user_login_pwd.login
        )
        if not user_or_none:
            raise UserNotFound
        verified = self.password_hasher.verify_password_hash(
            hashed_password_and_salt=PasswordHashAndSalt(
                password_hash=user_or_none.password_hash,
                salt=user_or_none.salt,
            ),
            password=user_login_pwd.password,
        )
        if verified:
            session_token = self.auth_token_controller.make_hex_token()
            await self.auth_user_repo.create_user_session(
                session_token=session_token,
                dt_created=self.dt_now,
                user_uuid=user_or_none.uuid,
            )
            return session_token
        return None


class UserAuthenticateBySession:
    def __init__(
        self,
        *,
        auth_user_repo: AuthUserRepo,
        dt_now: datetime.datetime,
        auth_token_controller: AuthTokenController,
    ):
        self.auth_user_repo = auth_user_repo
        self.auth_token_controller = auth_token_controller
        self.dt_now = dt_now

    async def authenticate_or_deny_user(
        self, user_session_token: str
    ) -> UserAuthSession:
        auth_session_or_none = await self.auth_user_repo.get_by_session_token(
            session_token=user_session_token
        )
        if not auth_session_or_none:
            raise UserSessionNotFoundOrExpired("not found")
        if not self.auth_token_controller.check_expired(
            dt_now=self.dt_now, last_login_dt=auth_session_or_none.session.last_login
        ):
            raise UserSessionNotFoundOrExpired("expired")
        return auth_session_or_none
