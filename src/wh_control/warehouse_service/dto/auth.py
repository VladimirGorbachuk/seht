from dataclasses import dataclass
from uuid import UUID

from warehouse_service.entities.vo import Login, Password


class UserLoginPwd:
    login: Login = Login()
    password: Password = Password()

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password


class UserLoginPwdUUID:
    uuid: UUID
    login: Login = Login()
    password: Password = Password()

    def __init__(self, login: str, password: str, uuid: UUID):
        self.login = login
        self.password = password
        self.uuid = uuid
