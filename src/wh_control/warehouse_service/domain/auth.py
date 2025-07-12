from dataclasses import dataclass
from uuid import UUID


class UserAuth:
    uuid: UUID
    login: str
    password: str
