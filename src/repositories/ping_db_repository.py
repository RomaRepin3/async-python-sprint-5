from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import app_logger


class PingDbRepository:
    """
    Репозиторий для проверки подключения к БД.
    """

    @staticmethod
    async def ping(db: AsyncSession) -> float:
        """
        Проверка подключения к БД.
        """
        app_logger.info('Ping db...')

        try:
            start_datetime = datetime.now()
            await db.execute(select(1))
            return (datetime.now() - start_datetime).total_seconds()
        except Exception as e:
            app_logger.exception(f'Ping db error: {e}')
            return 0.0
