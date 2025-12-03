from functools import lru_cache
from pydantic import Field,field_validator
from pydantic_settings import BaseSettings
from enum import Enum

class RunMode(str, Enum):
    """
    当前运行环境枚举值
    """
    DEV = "dev"
    TEST = "test"
    PROD = "prod"

    def is_prod(self) -> bool:
        return self.value == RunMode.PROD

    def is_dev(self) -> bool:
        return self.value == RunMode.DEV
    def is_test(self) -> bool:
        return self.value == RunMode.TEST

class Settings(BaseSettings):
    env : RunMode = Field(RunMode.DEV,alias="ENV")
    log_level : str = Field("INFO",alias="LOG_LEVEL")
    database_url: str = Field(...,alias="DATABASE_URL")
    secret_key: str = Field(...,alias="SECRET_KEY") # 密码加密秘钥
    algorithm: str = Field("HS256",alias="ALGORITHM") # 密码加密方法
    access_token_expire_minutes: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES") # jwt有效期

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        use_enum_values = True
        validate_default = True

    @field_validator("env", mode="before")
    def normalize_env(cls, v):
        if isinstance(v, str):
            return v.strip().lower()
        return v

    @property
    def is_dev(self) -> bool:
        return self.env == RunMode.DEV

    @property
    def is_test(self) -> bool:
        return self.env == RunMode.TEST
    @property
    def is_prod(self) -> bool:
        return self.env == RunMode.PROD


@lru_cache(maxsize=None)
def get_settings() -> Settings:
    return Settings()

settings = get_settings()