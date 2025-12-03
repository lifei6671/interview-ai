from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env : str = Field("dev",alias="ENV")
    log_level : str = Field("INFO",alias="LOG_LEVEL")
    database_url: str = Field(...,alias="DATABASE_URL")
    secret_key: str = Field(...,alias="SECRET_KEY") # 密码加密秘钥
    algorithm: str = Field("HS256",alias="ALGORITHM") # 密码加密方法
    access_token_expire_minutes: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES") # jwt有效期

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache(maxsize=None)
def get_settings() -> Settings:
    return Settings()

settings = get_settings()