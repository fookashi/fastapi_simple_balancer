from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic import Field


class AppSettings(PydanticBaseSettings):
    pg_host: str = Field(default="localhost", validation_alias="POSTGRES_HOST")
    pg_port: int = Field(default=5432, validation_alias="POSTGRES_PORT")
    pg_db: str = Field(default="balancer", validation_alias="POSTGRES_DB")
    pg_user: str = Field(default="balancer", validation_alias="POSTGRES_USER")
    pg_password: str = Field(default="balancer", validation_alias="POSTGRES_PASSWORD")
    pg_pool_size: int = Field(default=10, validation_alias="POSTGRES_POOL_SIZE")
    pg_max_overflow: int = Field(default=10, validation_alias="POSTGRES_MAX_OVERFLOW")

    redis_host: str = Field(default="localhost", validation_alias="REDIS_HOST")
    redis_port: int = Field(default=6379, validation_alias="REDIS_PORT")
    redis_db: int = Field(default=0, validation_alias="REDIS_DB")

    @property
    def pg_dsn(self) -> str:
        return f"postgresql://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_db}"

    @property
    def redis_dsn(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    class Config:
        env_file = ".env"
        extra = "forbid"
