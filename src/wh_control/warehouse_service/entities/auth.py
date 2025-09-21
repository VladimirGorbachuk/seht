from dataclasses import dataclass
from enum import StrEnum
from typing import NewType
from uuid import UUID
import datetime


Salt = NewType("Salt", bytes)
PasswordHash = NewType("PasswordHash", bytes)


@dataclass
class UserAuth:
    uuid: UUID
    login: str
    salt: Salt
    password_hash: PasswordHash

    def create_related_session(
        self, *, login_dt: datetime.datetime, session_token: str
    ) -> "UserAuthSession":
        """use in successful auth scenario, e.g. if password matches"""
        session = AuthSession(
            session_token=session_token, last_login=login_dt, user_uuid=self.uuid
        )
        return UserAuthSession(uuid=self.uuid, session=session)


@dataclass
class AuthSession:
    user_uuid: UUID
    session_token: str
    last_login: datetime.datetime


class GlobalPermissionEnum(StrEnum):
    """
    company-level permissions equivalent of superuser role,
    better switch to more fine-grained permissions
    """

    CAN_ADD_USER = "can add other users"
    CAN_ADD_WAREHOUSE = "can add warehouse"


@dataclass
class Permission:
    permission: GlobalPermissionEnum


@dataclass
class UserAuthSession:
    """
    currently contains only global permissions, would later add other fine-grained rbac
    """

    uuid: UUID
    session: AuthSession
    permissions: tuple[GlobalPermissionEnum]
