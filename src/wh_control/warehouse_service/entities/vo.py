from typing import Any


class LoginTooShort(ValueError):
    pass


class LoginTypeError(ValueError):
    pass


class LoginShouldContainNonNumericCharacters(ValueError):
    pass


class PasswordTooShort(ValueError):
    pass


class PasswordTypeError(ValueError):
    pass


class PasswordShouldContainNonNumericCharacters(ValueError):
    pass


class PasswordShouldContainNonAlphabetCharacters(ValueError):
    pass


LOGIN_MIN_LENGTH = 5
PASSWORD_MIN_LENGTH = 7


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
        if len(value) < LOGIN_MIN_LENGTH:
            raise LoginTooShort(f"login should be at least {LOGIN_MIN_LENGTH} chars")
        if value.isnumeric():
            raise LoginShouldContainNonNumericCharacters(
                "login should contain not only numeric characters"
            )

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


class Password:
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
            raise PasswordTypeError(f"expecting str, got {value}")
        if len(value) < PASSWORD_MIN_LENGTH:
            raise PasswordTooShort(
                f"password should be at least {PASSWORD_MIN_LENGTH} chars"
            )
        if value.isnumeric():
            raise PasswordShouldContainNonNumericCharacters(
                "should contain non numeric chars"
            )
        if value.isalpha():
            raise PasswordShouldContainNonAlphabetCharacters(
                "should contain nonalphabet chars also"
            )

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
