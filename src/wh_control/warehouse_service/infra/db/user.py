
from sqlalchemy import Table, Column, String, LargeBinary, UUID as SQLUUID, ForeignKey
from sqlalchemy.orm import registry

from warehouse_service.domain.auth import UserAuth

# Create a registry
mapper_registry = registry()
Base = mapper_registry.generate_base()

# AuthUser table definition
auth_user_table = Table(
    "auth_user",
    mapper_registry.metadata,
    Column("uuid", SQLUUID, primary_key=True),
    Column("login", String, unique=True),
    Column("salt", LargeBinary),
    Column("password_hash", LargeBinary),
)

# Permission table definition
permission_table = Table(
    "rbac_permission",
    mapper_registry.metadata,
    Column("name", String, primary_key=True),
)

# Association table for many-to-many relationship
user_permission_table = Table(
    "auth_user_permission",
    mapper_registry.metadata,
    Column("user_uuid", SQLUUID, ForeignKey("auth_user.uuid"), primary_key=True),
    Column("permission_name", String, ForeignKey("rbac_permission.name"), primary_key=True),
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