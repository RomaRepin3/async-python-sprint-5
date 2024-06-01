from aiobotocore.client import AioBaseClient
from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import PingDbRepository
from repositories import RedisRepository
from repositories import S3Repository
from schemas import PingResponseSchema
from utils import PingResponseSchemaRowMapper


async def get_ping(session: AsyncSession, redis: Redis, s3_client: AioBaseClient) -> PingResponseSchema:
    """
    Проверка соединения.

    :param session: Сессия БД.
    :param redis: Redis-коннектор.
    :param s3_client: Клиент S3.
    :return: Модель PingResponseSchema.
    """
    return await PingResponseSchemaRowMapper.map(
        db_ping=await PingDbRepository.ping(session),
        redis_ping=await RedisRepository.ping(redis),
        s3_ping=await S3Repository.ping(s3_client)
    )
