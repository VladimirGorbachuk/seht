import asyncio
import os
from logging import getLogger
from uuid import uuid4

from warehouse_service.interactors.auth import UserAlreadyExists
from warehouse_service.factories.auth import user_create_initialize
from warehouse_service.infra.db.sessionmaker import (
    async_sessionmaker_from_env,
)
from warehouse_service.configure_logging import configure_logger
from warehouse_service.dto.auth import UserLoginPwdUUID


configure_logger()

logger = getLogger(__name__)


async def create_user():
    logger.info("starting to create default user")
    if os.environ.get("DEFAULT_USER_LOGIN") and os.environ.get("DEFAULT_USER_PASSWORD"):
        default_user = UserLoginPwdUUID(
            uuid=uuid4(),
            login=os.environ["DEFAULT_USER_LOGIN"],
            password=os.environ["DEFAULT_USER_PASSWORD"],
        )
        logger.info("creating default user")
        sessionmaker = async_sessionmaker_from_env()
        async with sessionmaker() as session:
            interactor = user_create_initialize(session)
            try:
                await interactor.create_user(user_login_pwd=default_user)
                await session.commit()
            except UserAlreadyExists:
                logger.info("Already exists")
            logger.info("created_successfully")
        return
    raise ValueError(
        "provide 'DEFAULT_USER_LOGIN' and 'DEFAULT_USER_PASSWORD' env variables"
    )


def create_default_user():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(create_user())
