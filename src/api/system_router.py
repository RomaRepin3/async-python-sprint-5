from http import HTTPStatus
from typing import Annotated

from aiobotocore.client import AioBaseClient
from aioredis import Redis
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from depends import get_db_session
from depends import get_redis_connection
from depends import s3_client_dependency
from handlers import get_ping
from schemas import PingResponseSchema

system_router = APIRouter(
    tags=[
        'System',
    ]
)


@system_router.get(
    '/ping',
    response_model=PingResponseSchema,
    status_code=HTTPStatus.OK,
    name='Статус активности связанных сервисов'
)
async def ping(
        session: Annotated[AsyncSession, Depends(get_db_session)],
        redis: Annotated[Redis, Depends(get_redis_connection)],
        s3_client: Annotated[AioBaseClient, Depends(s3_client_dependency)]
) -> PingResponseSchema:
    return await get_ping(session=session, redis=redis, s3_client=s3_client)
