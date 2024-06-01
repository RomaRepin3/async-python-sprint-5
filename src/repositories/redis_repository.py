from datetime import datetime
from pickle import dumps
from pickle import loads
from typing import Any
from typing import Dict

from aioredis import Redis

from core import app_logger
from .base_repository import BaseRepository


class RedisRepository(BaseRepository):
    """
    Репозиторий для работы с Redis.
    """

    @staticmethod
    async def get(redis: Redis, key: str) -> Any:
        """
        Получение значения по ключу.

        :param redis: Подключение к Redis.
        :param key: Ключ.
        :return: Значение.
        """
        result = await redis.get(key)
        if result:
            result_loads = loads(result)
            app_logger.info(f'Redis get. Key: {key}, Value: {result_loads}')
            return result_loads
        app_logger.info(f'Redis get. Key: {key}, Value: None')
        return None

    @staticmethod
    async def get_multi(redis: Redis) -> Dict[str, Any]:
        """
        Получение сех ключей и занчений.

        :param redis: Подключение к Redis.
        :return: Словарь с ключами и значениями.
        """
        app_logger.info('Redis start get all keys')
        all_keys = await redis.keys('*')
        result = dict()
        for key in all_keys:
            result[key] = await redis.get(key)
        app_logger.info(f'Redis get all keys. Result: {result}')
        return result

    @classmethod
    async def create(cls, redis: Redis, key: str, value: Any, lifetime: int) -> None:
        """
        Установка значения по ключу.

        :param redis: Подключение к Redis.
        :param key: Ключ.
        :param value: Значение.
        :param lifetime: Время жизни в секундах.
        :return: None.
        """
        app_logger.info(f'Redis set. Key: {key}, Value: {value}, Lifetime: {lifetime}')
        await redis.set(key, dumps(value), ex=lifetime)

    @classmethod
    async def update(cls, redis: Redis, key: str, value: Any, lifetime: int) -> None:
        """
        Обновление значения по ключу.

        :param redis: Подключение к Redis.
        :param key: Ключ.
        :param value: Значение.
        :param lifetime: Время жизни в секундах.
        :return: None.
        """
        app_logger.info(f'Redis update. Key: {key}, Value: {value}, Lifetime: {lifetime}')
        await cls.create(redis, key, value, lifetime)

    @staticmethod
    async def delete(redis: Redis, key: str) -> None:
        """
        Удаление значения по ключу.

        :param redis: Подключение к Redis.
        :param key: Ключ.
        :return: None.
        """
        app_logger.info(f'Redis delete. Key: {key}')
        await redis.delete(key)

    @staticmethod
    async def ping(redis: Redis) -> float:
        """
        Пинг Redis.

        :param redis: Подключение к Redis.
        :return: Время пинга в секундах.
        """
        app_logger.info('Redis ping...')

        try:
            start_datetime = datetime.now()
            result = await redis.ping()
            delay = (datetime.now() - start_datetime).total_seconds()
            if result == b'PONG':
                app_logger.info(f'Redis ping. Result: {result}, Delay: {delay}')
            else:
                app_logger.warning(f'Redis ping. Invalid result: {result}, Delay: {delay}')
            return delay
        except Exception as e:
            app_logger.exception(f'Redis ping error: {e}')
            return 0.0
