from datetime import datetime
from typing import Any

from aiobotocore.client import AioBaseClient
from fastapi import File

from core import app_logger
from core import app_settings
from .base_repository import BaseRepository


class S3Repository(BaseRepository):
    """
    Репозиторий для работы с S3.
    """

    @staticmethod
    async def get(s3_client: AioBaseClient, key: str) -> Any:
        """
        Загрузка объекта из S3.

        :param s3_client: S3-клиент.
        :param key: Ключ.
        :return: Загруженный объект.
        """
        app_logger.info(f'Get object from S3: {key}')
        return await s3_client.get_object(Bucket=app_settings.S3_BUCKET, Key=key)

    @staticmethod
    async def get_multi():
        pass

    @staticmethod
    async def create(s3_client: AioBaseClient, key: str, file_object: File) -> None:
        """
        Загрузка объекта в S3.

        :param s3_client: S3-клиент.
        :param key: Ключ.
        :param file_object: Объект.
        :return: Результат загрузки.
        """
        try:
            app_logger.info(f'Upload file to S3: {key}')
            await s3_client.upload_fileobj(file_object, Bucket=app_settings.S3_BUCKET, Key=key)
            app_logger.info('Upload file to S3 is OK!')
        except Exception as e:
            app_logger.error(f'Upload file {key} to S3 error: {type(e)} {e}')

    @staticmethod
    async def update():
        pass

    @staticmethod
    async def delete():
        pass

    @staticmethod
    async def ping(s3_client: AioBaseClient) -> float:
        """
        Пинг S3.

        :param s3_client: S3-клиент.
        :return: Время пинга в секундах.
        """
        try:
            start_datetime = datetime.now()
            result = await s3_client.list_buckets()
            if result:
                app_logger.info(f'S3 ping. Result: {result}, Delay: {start_datetime}')
            else:
                app_logger.warning(f'S3 ping. Invalid result: {result}, Delay: {start_datetime}')
            return (datetime.now() - start_datetime).total_seconds()
        except Exception as e:
            app_logger.exception(f'S3 ping error: {e}')
            return 0.0
