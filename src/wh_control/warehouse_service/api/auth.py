from fastapi import APIRouter, Depends, HTTPException, status

from .dependencies import UserAuthenticateProtocol, UserCreateProtocol
from warehouse_service.interactors.auth import UserNotFound
from warehouse_service.dto.auth import UserLoginPwd, UserLoginPwdUUID


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("user", status_code=status.HTTP_201_CREATED)
async def add_user(
    user_data: UserLoginPwdUUID,
    user_create: UserCreateProtocol = Depends(),
):
    """Create a new user account (and should add check if permissions allow)"""
    await user_create.create_user(user_data)
    return {"message": "User created successfully"}


@router.post("login")
async def login_user(
    credentials: UserLoginPwd,
    user_authenticate: UserAuthenticateProtocol = Depends(),
):
    try:
        is_authenticated = await user_authenticate.authenticate_or_deny_user(
            credentials
        )
        if not is_authenticated:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
            )
        return {"message": "Login successful"}
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
