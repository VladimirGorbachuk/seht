from pydantic import BaseModel

from warehouse_service.dto.auth import UserLoginPwd


class UserLoginPwdSerializer(BaseModel):
    login: str
    password: str

    def to_dataclass(self) -> UserLoginPwd:
        return UserLoginPwd(self.login, self.password)