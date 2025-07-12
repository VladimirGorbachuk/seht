from warehouse_service.application.auth import PasswordHasher
from warehouse_service.infra.db.user import AuthUser
from warehouse_service.serializers.auth import UserLoginPwd

class UserAuthenticate:
    def __init__(self, password_hasher: PasswordHasher):
        self.password_hasher = password_hasher

    async def authenticate_user(self, user_login_pwd: UserLoginPwd):
        password_salt_and_hash = self.password_hasher.hash_password(user_login_pwd.password)
        user = AuthUser(
            login = user_login_pwd.login,
            salt=password_salt_and_hash.salt,
            password_hash=password_salt_and_hash.password_hash,
        )