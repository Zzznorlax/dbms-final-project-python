from functools import lru_cache
import secrets
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


POSTGRES_PATH_FORMAT = "/{}"


class Settings(BaseSettings):

    PROJECT_NAME: str

    JWT_SECRET: str = secrets.token_urlsafe(32)
    JWT_ALGO: str = "HS256"

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    SERVER_NAME: str
    SERVER_HOST: str
    SERVER_PORT: str = "8080"

    API_V1_STR: str = "/api/v1"

    IMGUR_API_URL: str
    IMGUR_API_CLIENT_ID: str

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    SQLALCHEMY_DATABASE_URI: str

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings(env_path: str = ".env") -> Settings:
    return Settings(_env_file=env_path)