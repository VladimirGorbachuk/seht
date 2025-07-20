from sqlalchemy.ext.asyncio import AsyncSession

from warehouse_service.interactors.auth import UserAuthenticate, UserCreate, UserAuthenticateBySession
from warehouse_service.repository.auth_user import AuthUserRepo
from warehouse_service.application.auth import PasswordHasher, AuthCryptoSettings, SessionTokenCreator


def user_authenticate_from_session(sess: AsyncSession, auth_crypto_settings: AuthCryptoSettings) -> UserAuthenticate:
    hasher = PasswordHasher(auth_crypto_settings)
    auth_session_creator = SessionTokenCreator(auth_crypto_settings)
    auth_repo = AuthUserRepo(sess)
    return UserAuthenticate(password_hasher=hasher, auth_user_repo=auth_repo, auth_session_creator=auth_session_creator)


def user_create_from_session(sess: AsyncSession, auth_crypto_settings: AuthCryptoSettings) -> UserCreate:
    hasher = PasswordHasher(auth_crypto_settings)
    auth_repo = AuthUserRepo(sess)
    return UserCreate(password_hasher=hasher, auth_user_repo=auth_repo)


def session_auth_from_session(sess: AsyncSession) -> UserAuthenticateBySession:
    auth_repo = AuthUserRepo(sess)
    return UserAuthenticateBySession(auth_user_repo=auth_repo)
