import datetime

from warehouse_service.application.auth import PasswordHashAndSalt, PasswordHasher, SessionTokenCreator
from warehouse_service.domain.auth import UserAuthSession
from warehouse_service.serializers.auth import UserLoginPwd, UserLoginPwdUUID
from warehouse_service.repository.auth_user import AuthUserRepo


class UserNotFound(Exception):
    pass


class UserSessionNotFoundOrExpired(Exception):
    pass


class UserCreate:
    def __init__(self, *, password_hasher: PasswordHasher, auth_user_repo: AuthUserRepo):
        self.password_hasher = password_hasher
        self.auth_user_repo = auth_user_repo

    async def create_user(self, user_login_pwd: UserLoginPwdUUID):
        password_salt_and_hash = self.password_hasher.hash_password(user_login_pwd.password)
        await self.auth_user_repo.add_user(
            uuid=user_login_pwd.uuid,
            login = user_login_pwd.login,
            salt=password_salt_and_hash.salt,
            password_hash=password_salt_and_hash.password_hash,
        )


class UserAuthenticate:
    def __init__(
        self,
        *,
        password_hasher: PasswordHasher,
        auth_user_repo: AuthUserRepo,
        auth_session_creator: SessionTokenCreator,
        dt_now: datetime.datetime,
    ):
        self.password_hasher = password_hasher
        self.auth_user_repo = auth_user_repo
        self.auth_session_creator = auth_session_creator
        self.dt_now = dt_now

    async def authenticate_or_deny_user(self, user_login_pwd: UserLoginPwd) -> str:
        user_or_none = await self.auth_user_repo.get_by_login(login=user_login_pwd.login)
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
            session_token = self.auth_session_creator.make_hex_token()
            await self.auth_user_repo.create_user_session(
                session_token=session_token, 
                dt_created=self.dt_now,
                user_uuid=user_or_none.uuid,
            )
            return session_token
        return None


class UserAuthenticateBySession:
    def __init__(self, *, auth_user_repo: AuthUserRepo, dt_now: datetime.datetime):
        self.auth_user_repo = auth_user_repo
        self.dt_now = dt_now

    async def authenticate_or_deny_user(self, user_session_token: str) -> UserAuthSession:
        # todo: need to amend current dt here!
        user_or_none = await self.auth_user_repo.get_by_session_token(session_token=user_session_token)
        if not user_or_none:
            raise UserSessionNotFoundOrExpired
        return user_or_none