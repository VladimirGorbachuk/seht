
from sqlalchemy import Table, Column, String, LargeBinary, UUID as SQLUUID, ForeignKey, DateTime
from sqlalchemy.orm import registry, relationship

from warehouse_service.domain.auth import UserAuth, UserAuthSession, AuthSession, Permission

# Create a registry
mapper_registry = registry()
Base = mapper_registry.generate_base()


auth_user_table = Table(
    "auth_user",
    mapper_registry.metadata,
    Column("uuid", SQLUUID, primary_key=True),
    Column("login", String, unique=True),
    Column("salt", LargeBinary),
    Column("password_hash", LargeBinary),
)


user_session_table = Table(
    "auth_session",
    mapper_registry.metadata,
    Column("session_token", String, primary_key=True),
    Column("user_uuid", SQLUUID, ForeignKey("auth_user.uuid", ondelete="CASCADE"), nullable=False),
    Column("last_login", DateTime, nullable=False)
)


permission_table = Table(
    "global_permission",
    mapper_registry.metadata,
    Column("name", String, primary_key=True),
)


user_permission_table = Table(
    "auth_user_permission",
    mapper_registry.metadata,
    Column("user_uuid", SQLUUID, ForeignKey("auth_user.uuid", ondelete="CASCADE"), primary_key=True),
    Column("permission_name", String, ForeignKey("global_permission.name"), primary_key=True),
)



mapper_registry.map_imperatively(
    UserAuth,
    auth_user_table,
    properties={
        'uuid': auth_user_table.c.uuid,
        'login': auth_user_table.c.login,
        'salt': auth_user_table.c.salt,
        'password_hash': auth_user_table.c.password_hash,
    }
)


mapper_registry.map_imperatively(
    AuthSession,
    user_session_table,
    properties={
        "user_uuid": user_session_table.c.user_uuid,
        "session_token": user_session_table.c.session_token,
        "last_login": user_session_table.c.last_login,
    }
)



mapper_registry.map_imperatively(
    Permission,
    permission_table,
    properties = {
        "permission": permission_table.c.name
    }
)


mapper_registry.map_imperatively(
    UserAuthSession,
    auth_user_table,
    properties={
        "session": relationship(AuthSession, backref="auth_user_table", uselist=False),
        "permissions": relationship(Permission, secondary="auth_user_permission", backref="global_permission")
    },
)
