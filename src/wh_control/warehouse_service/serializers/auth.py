from uuid import UUID

from pydantic import BaseModel


class UserLoginPwd(BaseModel):
    login: str
    password: str


class UserLoginPwdUUID(BaseModel):
    uuid: UUID
    login: str
    password: str
