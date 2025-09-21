from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from testcontainers.postgres import PostgresContainer

from warehouse_service.infra.db.settings import PostgresSettings
from warehouse_service.interactors.auth import (
    UserNotFound,
    UserSessionNotFoundOrExpired,
)
from warehouse_service.dto.auth import UserLoginPwd, UserLoginPwdUUID

from warehouse_service.factories.auth import (
    user_authenticate_initialize,
    user_create_initialize,
    session_auth_initialize,
)
from warehouse_service.application.auth import AuthCryptoSettings

