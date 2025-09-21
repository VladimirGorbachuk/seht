from dataclasses import dataclass, field
from typing import Any


class LoginTooShort(ValueError):
    pass


class LoginTypeError(ValueError):
    pass



class Login:
    """
    use both as VO and as descriptor
    """
    def __init__(self, value: str | None = None):
        if value is not None:
            self._validate(value)
        self._value = value

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = f"private__{name}"

    def _validate(self, value: str) -> None:
        if not isinstance(value, str):
            raise LoginTypeError(f"expecting str, got {value}")
        if len(value) < 5:
            raise LoginTooShort("login should be at least 5 chars")
            
    def __set__(self, obj, value: "str | Login"):
        if isinstance(value, Login):
            setattr(obj, self.private_name, value._value)
            return
        self._validate(value)
        setattr(obj, self.private_name, value)
        
    def __get__(self, instance, cls) -> str:
        return getattr(instance, self.private_name)
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Login):
            return False
        return self._value == other._value

class Auth:
    login: Login = Login()
    
    def __init__(self, login: str):
        self.login = login

    def __eq__(self, other):
        if not isinstance(other, Auth):
            return False
        print(self.login, other.login, self.login == other.login)
        return self.login == other.login
    

@dataclass(frozen=True, slots=True, eq=True)
class AuthDt:
    login: Login = field(default_factory=Login)




first = Auth(login = Login("aaaaaa"))
print(first.login, "ok - 1")
second = Auth(login="abcdef")
print(second.login, "ok - 2")


assert Auth(login = Login("aaaaaa")) == Auth(login="aaaaaa")

try:
    print('and here should fail:')
    Auth(login="abc")
except LoginTooShort as e:
    print("expected exception", e)



try:
    print('and here should fail too:')
    Login("abc")
except LoginTooShort as e:
    print("expected exception 2", e)


try:
    print('and here should fail also:')
    Login(b"abc")
except LoginTypeError as e:
    print("expected exception 3", e)



print("here comes the dataclass(")
first = AuthDt(login = Login("aaaaaa"))
print(first.login, "ok - 1")
second = AuthDt(login="abcdef")
print(second.login, "ok - 2")


assert AuthDt(login = "bbbb") == AuthDt(login="bbbb")
assert AuthDt(login = Login("aaaaaa")) == AuthDt(login=Login("aaaaaa"))
assert AuthDt(login = Login("aaaaaa")) != AuthDt(login=Login("aaaaaab"))

try:
    print('and here should fail?:')
    AuthDt(login="abc")
    print('unfortunately it is ok...')
except LoginTooShort as e:
    print("expected exception", e)   # here we have no fail

