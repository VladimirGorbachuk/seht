from logging import getLogger

from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from .dependencies import UserAuthenticateProtocol, UserCreateProtocol
from .serializers import UserLoginPwdSerializer
from warehouse_service.interactors.auth import (
    UserNotFound,
    UserVerifyFailed,
    UserAuthenticateBySessionProtocol,
    UserSessionNotFoundOrExpired,
)
from warehouse_service.dto.auth import UserLoginPwdUUID


logger = getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/user", status_code=status.HTTP_201_CREATED)
async def add_user(
    user_data: UserLoginPwdUUID,
    user_create: UserCreateProtocol = Depends(),
    user_auth_by_session: UserAuthenticateBySessionProtocol = Depends(),
    sessionid: str | None = Cookie(None),
) -> JSONResponse:
    """Create a new user account (and should add check if permissions allow)"""
    logger.info("got following sessionid %s", sessionid)
    if not sessionid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="no session cookie",
        )
    try:
        user = await user_auth_by_session.authenticate_or_deny_user(sessionid)
        logger.info("user is %s", user)
    except UserSessionNotFoundOrExpired as e:
        logger.exception("caught %s", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired",
        )
    await user_create.create_user(user_data)
    return JSONResponse(
        {"message": "user_created", "success": True},
        status_code=status.HTTP_201_CREATED,
    )


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    credentials: UserLoginPwdSerializer,
    user_authenticate: UserAuthenticateProtocol = Depends(),
):
    dto = credentials.to_dataclass()
    try:
        session_token = await user_authenticate.authenticate_or_deny_user(
            dto,
        )
        response = JSONResponse(
            content={"message": "Login successful", "success": True},
            status_code=status.HTTP_200_OK,
        )
        response.set_cookie(
            key="sessionid",
            value=session_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=3600,
            path="/",
        )
        return response
    except UserNotFound:
        return JSONResponse(
            {"message": "User not found", "success": False},
            status_code=status.HTTP_200_OK,
        )
    except UserVerifyFailed:
        return JSONResponse(
            {"message": "wrong user", "success": False},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("WTF %s", e)
        return JSONResponse({"message": "unexpected", "success": False})
