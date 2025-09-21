import os

from alembic import command
from alembic.config import Config

from warehouse_service.infra.db.settings import PostgresSettings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ALEMBIC_INI_LOCATION = os.path.join(BASE_DIR, "alembic.ini")
ALEMBIC_SCRIPT_LOCATION = os.path.dirname(os.path.abspath(__file__))

COMMAND_DISPATCH_DICT = {
    "upgrade": command.upgrade,
    "downgrade": command.downgrade,
    "revision": command.revision,
    "current": command.current,
    "history": command.history,
    "heads": command.heads,
    "branches": command.branches,
    "stamp": command.stamp,
    "show": command.show,
    "check": command.check,
    "merge": command.merge,
    "edit": command.edit,
    "ensure_version": command.ensure_version,
    "list_templates": command.list_templates,
    "init": command.init,
}


def init_alembic_config(settings: PostgresSettings) -> Config:
    alembic_config = Config(ALEMBIC_INI_LOCATION)
    alembic_config.set_main_option("script_location", ALEMBIC_SCRIPT_LOCATION)
    alembic_config.set_main_option("sqlalchemy.url", settings.full_url)
    return alembic_config


def upgrade(settings: PostgresSettings | None = None) -> None:
    if settings is None:
        settings = PostgresSettings.from_env()
    print("GOING TO UPGRADE")
    command.upgrade(config=init_alembic_config(settings), revision="head")
    print("UPGRADED")
