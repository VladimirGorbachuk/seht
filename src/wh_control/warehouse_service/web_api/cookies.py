from dataclasses import dataclass
from typing import Protocol
import os

from fastapi.responses import JSONResponse


@dataclass(frozen=True, slots=True)
class CookieSettings:
    max_age: int
    secure: bool = True

    @classmethod
    def initialize_from_environment(cls) -> "CookieSettings":
        use_insecure_cookies = os.environ.get("COOKIES_INSECURE_ONLY_LOCAL", False) == "True"
        return cls(
            max_age = int(os.environ.get("COOKIES_MAX_AGE", 3600)),
            secure = not use_insecure_cookies,
        )


class ResponseCookieManagerProtocol(Protocol):
    def set_cookie(self, response: JSONResponse, session_token: str) -> JSONResponse:
        pass


class ResponseCookieManager:
    def __init__(self, settings: CookieSettings):
        self._settings = settings

    def set_cookie(self, response: JSONResponse, session_token: str) -> JSONResponse:
        response.set_cookie(
            key="sessionid",
            value=session_token,
            httponly=True,
            secure=self._settings.secure,
            samesite="strict",
            max_age=self._settings.max_age,
            path="/",
        )
        return response


