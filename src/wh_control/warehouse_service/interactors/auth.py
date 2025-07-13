from warehouse_service.application.auth import PasswordHashAndSalt, PasswordHasher
from warehouse_service.serializers.auth import UserLoginPwd
from warehouse_service.repository.auth_user import AuthUserRepo
from warehouse_service.infra.db.sessionmaker import PostgresSessions


class UserNotFound(Exception):
    pass


class UserCreate:
    def __init__(self, *, password_hasher: PasswordHasher, auth_user_repo: AuthUserRepo):
        self.password_hasher = password_hasher
        self.auth_user_repo = auth_user_repo

    async def create_user(self, user_login_pwd: UserLoginPwd):
        password_salt_and_hash = self.password_hasher.hash_password(user_login_pwd.password)
        await self.auth_user_repo.add_user(
            login = user_login_pwd.login,
            salt=password_salt_and_hash.salt,
            password_hash=password_salt_and_hash.password_hash,
        )


class UserAuthenticate:
    def __init__(self, *, password_hasher: PasswordHasher, auth_user_repo: AuthUserRepo):
        self.password_hasher = password_hasher
        self.auth_user_repo = auth_user_repo

    async def authenticate_or_deny_user(self, user_login_pwd: UserLoginPwd) -> bool:
        user_or_none = await self.auth_user_repo.get_by_login(login=user_login_pwd.login)
        if not user_or_none:
            raise UserNotFound
        return self.password_hasher.verify_password_hash(
            hashed_password_and_salt=PasswordHashAndSalt(
                password_hash=user_or_none.password_hash,
                salt=user_or_none.salt,
            ), 
            password=user_login_pwd.password,
        )

        