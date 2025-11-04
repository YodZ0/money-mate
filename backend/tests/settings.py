from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent  # tests


class DatabaseConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    name: str
    provider: str = "postgresql+asyncpg"

    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 50

    @property
    def dsn(self) -> str:
        return f"{self.provider}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        env_file=(BASE_DIR / ".env"),
        extra="ignore",
    )
    base_dir: Path = BASE_DIR
    db: DatabaseConfig


settings = Settings()
