from typing import Generator

import pytest

from warehouse_service.application.auth import PasswordHasher, PasswordHashSettings


@pytest.fixture
def password_hasher() -> Generator[PasswordHasher, None, None]:
    settings = PasswordHashSettings.initialize_from_environment()
    yield PasswordHasher(settings)