from datetime import timedelta

from aioredis import Redis
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core import app_settings
from depends import user_repository
from repositories import RedisRepository
from schemas import TokenSchema
from utils import CommonUtils
from utils import ExceptionFactory


async def auth_user(user_data: OAuth2PasswordRequestForm, session: AsyncSession, redis: Redis) -> TokenSchema:
    """
    Авторизация пользователя.

    :param user_data: Данные пользователя.
    :param session: Сессия БД.
    :param redis: Redis-коннектор.
    :return: Токен авторизации.
    """
    user = await user_repository.get_by_login(db=session, login=user_data.username)
    if user and user and await CommonUtils.verify_password(user_data.password, user.password):
        access_token = await CommonUtils.create_access_token(
            data={
                'sub': user.login,
            },
            expires_delta=timedelta(minutes=app_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        await RedisRepository.create(
            redis=redis,
            key=access_token,
            value=user.id,
            lifetime=app_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        return TokenSchema(access_token=access_token)
    raise await ExceptionFactory.get_401_exception(f'Invalid credentials: {user_data}')
