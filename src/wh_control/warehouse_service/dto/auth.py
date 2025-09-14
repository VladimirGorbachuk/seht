from dataclasses import dataclass
from uuid import UUID

from warehouse_service.entities.auth import Password


@dataclass
class UserLoginPwd:
    login: str
    password: Password


@dataclass
class UserLoginPwdUUID:
    uuid: UUID
    login: str
    password: Password
