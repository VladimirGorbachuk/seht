from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserLoginPwd:
    login: str
    password: str


@dataclass
class UserLoginPwdUUID:
    uuid: UUID
    login: str
    password: str
