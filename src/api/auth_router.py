from http import HTTPStatus
from typing import Annotated

from aioredis import Redis
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from depends import get_db_session
from depends import get_redis_connection
from handlers import auth_user
from handlers import register_user
from schemas import OperationStatusResponseSchema
from schemas import TokenSchema
from schemas import UserRequestSchema

auth_router = APIRouter(tags=['Auth'])


@auth_router.post(
    '/register',
    response_model=OperationStatusResponseSchema,
    status_code=HTTPStatus.CREATED,
    name='Регистрация пользователя'
)
async def register(
        register_data: UserRequestSchema,
        session: Annotated[AsyncSession, Depends(get_db_session)]
) -> OperationStatusResponseSchema:
    return await register_user(register_data, session)


@auth_router.post(
    '/auth',
    response_model=TokenSchema,
    status_code=HTTPStatus.OK,
    name='Авторизация пользователя'
)
async def auth(
        auth_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Annotated[AsyncSession, Depends(get_db_session)],
        redis: Annotated[Redis, Depends(get_redis_connection)]
) -> TokenSchema:
    return await auth_user(auth_data, session, redis)
