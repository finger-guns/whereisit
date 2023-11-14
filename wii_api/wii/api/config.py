from enum import Enum
from functools import lru_cache
from json import loads
from os import getenv
from os.path import dirname, join

from pydantic import Field
from pydantic_settings import BaseSettings

from .schema.base import WhereIsItBaseModel


class EnvironmentTypes(str, Enum):
    LOCAL = "LOCAL"

    LOCAL_DEVELOPMENT = "LOCAL_DEVELOPMENT"
    LOCAL_USER_ACCEPTANCE_TESTING = "LOCAL_UAT"
    LOCAL_PRODUCTION = "LOCAL_PRODUCTION"

    DEVELOPMENT = "DEVELOPMENT"
    USER_ACCEPTANCE_TESTING = "USER_ACCEPTANCE_TESTING"
    PRODUCTION = "PRODUCTION"


def get_version() -> str:
    with open(join(dirname(__file__), "version.json"), "r") as f:
        version = loads(f.read())
        return version


class Settings(BaseSettings):
    SERVICE_NAME: str = "where_is_it"

    APP_BASE_URL: str = "/where_is_it/"
    APP_TITLE: str = "where_is_it"
    APP_VERSION: str = get_version()
    APP_DESCRIPTION: str = "Where is something streaming"

    VERBOSE_LOGGING: bool = True
    RETURN_EXCEPTION_REASON: bool = True

    BACKEND_ERROR_MESSAGE: str = "The backend encounted and error."
    DATABASE_ERROR_MESSAGE: str = "An error occured while accessing the database."

    ENVIRONMENT_TYPE: str = getenv(
        "ENVIRONMENT_TYPE",
        default=EnvironmentTypes.LOCAL,
    )

    DATABASE_HOST: str = Field(default="wii_db")
    DATABASE_USER: str = Field(default="wii")
    DATABASE_PASSWORD: str = Field(default="wii")
    DATABASE_NAME: str = Field(default="wii")
    DATABASE_PORT: str = Field(default="5432")

    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)

    USE_SSL: bool = False

    SSL_SERVER_CA_PATH: str = ""
    SSL_CERT_PATH: str = ""
    SSL_KEY_PATH: str = ""

    GOOGLE_APPLICATION_CREDENTIALS: str | None = None

    class Config:
        secrets_dir = "/etc/"


class WhereIsItLogConfig(WhereIsItBaseModel):
    LOGGER_NAME: str = "where_is_it"
    LOG_FORMAT: str = "%(levelprefix)s | %(path)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: dict = {
        "where_is_it": {"handlers": ["default"], "level": LOG_LEVEL},
    }


@lru_cache
def get_settings() -> "Settings":
    return Settings()
