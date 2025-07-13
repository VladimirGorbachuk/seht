from warehouse_service.application.auth import PasswordHashAndSalt, PasswordHasher
from warehouse_service.serializers.auth import UserLoginPwd
from warehouse_service.repository.auth_user import AuthUserRepo
from warehouse_service.infra.db.sessionmaker import PostgresSessions

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
        user = await self.auth_user_repo.get_by_login(login=user_login_pwd.login)
        return self.password_hasher.verify_password_hash(
            hashed_password_and_salt=PasswordHashAndSalt(
                password_hash=user.password_hash,
                salt=user.salt,
            ), 
            password=user_login_pwd.password,
        )


def default_user_authenticate_factory(*, async_sessionmaker: PostgresSessions, password_hasher: PasswordHasher):
    with async_sessionmaker() as sess:
        repo = AuthUserRepo(sess)
        yield UserAuthenticate(password_hasher=password_hasher, auth_user_repo=repo)
        

def default_user_create_factory(*, async_sessionmaker: PostgresSessions, password_hasher: PasswordHasher):
    with async_sessionmaker() as sess:
        repo = AuthUserRepo(sess)
        yield UserCreate(password_hasher=password_hasher, auth_user_repo=repo)
        