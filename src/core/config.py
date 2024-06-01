from logging import config as logging_config
from logging import getLogger

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

from .logger import LOGGING

logging_config.dictConfig(LOGGING)
app_logger = getLogger('app')


class AppSettings(BaseSettings):
    """
    Настройки приложения.
    """
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    PROJECT_NAME: str
    DATABASE_DSN: str
    PROJECT_HOST: str
    INTERNAL_PORT: int
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REDIS_DSN: str
    REDIS_PASSWORD: str
    S3_SERVICE_NAME: str
    S3_REGION_NAME: str
    S3_USE_SSL: bool
    S3_ENDPOINT_URL: str
    S3_AWS_ACCESS_KEY_ID: str
    S3_AWS_SECRET_ACCESS_KEY: str
    S3_BUCKET: str


app_settings = AppSettings()
