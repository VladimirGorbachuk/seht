from uuid import uuid4

import pytest
from testcontainers.postgres import PostgresContainer

from warehouse_service.infra.db.settings import PostgresSettings
from warehouse_service.interactors.auth import UserAuthenticate, UserCreate, UserNotFound, UserAuthenticateBySession
from warehouse_service.serializers.auth import UserLoginPwd, UserLoginPwdUUID


@pytest.mark.asyncio
async def test_settings_same(
        postgres_settings: PostgresSettings,
        postgres_container_with_migrations: PostgresContainer,
    ):
    conn_url = postgres_container_with_migrations.get_connection_url()
    assert conn_url == postgres_settings.full_url



@pytest.mark.asyncio
async def test_interactor_nonexisting_not_found(
        user_authenticate_interactor_with_rollback: UserAuthenticate,
    ):
    nonexisting = UserLoginPwd(login="testt", password="testt")
    with pytest.raises(UserNotFound):
        await user_authenticate_interactor_with_rollback.authenticate_or_deny_user(nonexisting)


@pytest.mark.asyncio
async def test_interactor_user_create(
        user_create_interactor_with_rollback: UserCreate,
        user_authenticate_interactor_with_rollback: UserAuthenticate,
    ):
    to_create = UserLoginPwdUUID(login="testt", password="testt", uuid=uuid4())
    to_check = UserLoginPwd(login=to_create.login, password=to_create.password)
    await user_create_interactor_with_rollback.create_user(to_create)
    assert await user_authenticate_interactor_with_rollback.authenticate_or_deny_user(to_check) is not None


@pytest.mark.asyncio
async def test_interactor_nonexisting_sess_cannot_auth(
    user_authenticate_by_session_with_rollback: UserAuthenticateBySession,
):
    await user_authenticate_by_session_with_rollback.authenticate_or_deny_user("not a real token")


# @pytest.mark.asyncio
# async def test_interactor_user_create_and_sess_auth(
#    user_authenticate_by_session_with_rollback: UserAuthenticateBySession,
#         user_authenticate_interactor_with_rollback: UserAuthenticate,
#     ):
#     to_create = UserLoginPwdUUID(login="testt", password="testt", uuid=uuid4())
#     to_check = UserLoginPwd(login=to_create.login, password=to_create.password)
#     await user_create_interactor_with_rollback.create_user(to_create)
#     assert await user_authenticate_interactor_with_rollback.authenticate_or_deny_user(to_check) is True
