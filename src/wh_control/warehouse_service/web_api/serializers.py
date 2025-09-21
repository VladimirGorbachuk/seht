from uuid import UUID

from pydantic import BaseModel

from warehouse_service.dto.auth import UserLoginPwd, UserLoginPwdUUID


class UserLoginPwdSerializer(BaseModel):
    login: str
    password: str

    def to_dto(self) -> UserLoginPwd:
        return UserLoginPwd(self.login, self.password)



class UserLoginPwdUUIDSerializer(BaseModel):
    login: str
    password: str
    uuid: UUID

    def to_dto(self) -> UserLoginPwdUUID:
        return UserLoginPwdUUID(self.login, self.password, uuid=self.uuid)