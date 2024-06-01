from typing import Annotated

from aioboto3 import Session
from aiobotocore.client import AioBaseClient
from aioredis import Redis
from aioredis import from_url
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from core import app_settings
from db import async_session
from models import FileModel
from models import UserModel
from repositories import FileRepository
from repositories import RedisRepository
from repositories import UserRepository

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth')

file_repository = FileRepository(FileModel)
user_repository = UserRepository(UserModel)

s3_session = Session()


async def get_db_session() -> AsyncSession:
    """
    Функция при внедрении зависимостей с БД.
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


async def get_redis_connection() -> Redis:
    """
    Функция при внедрении зависимостей с Redis.

    :return: Redis-коннектор.
    """
    return await from_url(app_settings.REDIS_DSN)


async def verify_token(
        token: Annotated[str, Depends(oauth2_scheme)],
        redis: Annotated[Redis, Depends(get_redis_connection)]
) -> str:
    """
    Проверка токена.

    :param token: Токен.
    :param redis: Redis-коннектор.
    :return: Результат проверки.
    """
    from utils import ExceptionFactory

    user_id = await RedisRepository.get(redis=redis, key=token)
    if not user_id:
        raise ExceptionFactory.get_401_exception(f'Invalid token: {token}')
    return user_id


async def get_s3_client() -> AioBaseClient:
    """
    Функция при внедрении зависимостей с S3.

    :return: S3-клиент.
    """
    return s3_session.client(
            service_name=app_settings.S3_SERVICE_NAME,
            region_name=app_settings.S3_REGION_NAME,
            use_ssl=app_settings.S3_USE_SSL,
            endpoint_url=app_settings.S3_ENDPOINT_URL,
            aws_access_key_id=app_settings.S3_AWS_ACCESS_KEY_ID,
            aws_secret_access_key=app_settings.S3_AWS_SECRET_ACCESS_KEY
    )


async def s3_client_dependency() -> AioBaseClient:
    """
    Функция при внедрении зависимостей с S3.

    :return: S3-клиент.
    """
    async with await get_s3_client() as s3_client:
        try:
            yield s3_client
        finally:
            await s3_client.close()
