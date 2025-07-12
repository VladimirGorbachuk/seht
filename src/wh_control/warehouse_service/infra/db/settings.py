from dataclasses import dataclass
import os


@dataclass(frozen=True, slots=True)
class PostgresSettings:
    user: str
    password: str
    host: str
    port: int
    db: str

    @classmethod
    def from_env(cls) -> "PostgresSettings":
        return cls(
            user=os.environ.get("POSTGRES_USER", "postgres"),
            password=os.environ.get("POSTGRES_PASSWORD", "postgres"),
            host=os.environ.get("POSTGRES_HOST", "postgres"),
            port=int(os.environ.get("POSTGRES_PORT", 5432)),
            db=os.environ.get("POSTGRES_DB", "default"),
        )

    @property
    def full_url(self) -> str:
        return "postgresql+psycopg://{user}:{password}@{host}:{port}/{db}".format(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            db=self.db,
        )
    


