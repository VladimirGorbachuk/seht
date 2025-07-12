from pydantic import BaseModel


class UserLoginPwd(BaseModel):
    login: str
    password: str
