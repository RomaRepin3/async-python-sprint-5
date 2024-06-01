from traceback import format_exc

from fastapi import HTTPException

from core import app_logger
from schemas import ExceptionResponseSchema


class ExceptionResponseSchemaRowMapper:
    """
    Сборка модели ответа исключения.
    """

    @staticmethod
    async def get_from_http_exception(exception: HTTPException) -> ExceptionResponseSchema:
        """
        Сборка модели ExceptionResponseSchema из HTTP исключения.

        :param exception: Объект исключения.
        :return: Модель ExceptionResponseSchema.
        """
        app_logger.info(f'Mapping http error json response: {exception.detail}')
        return ExceptionResponseSchema(
            exception=exception.detail,
            exception_traceback=list()
        )

    @staticmethod
    async def get_from_exception(exception: Exception) -> ExceptionResponseSchema:
        """
        Сборка модели ExceptionResponseSchema из исключения.

        :param exception: Объект исключения.
        :return: Модель ExceptionResponseSchema.
        """
        app_logger.error(f'Mapping unexpected error json response: {exception}')
        traceback = format_exc(chain=False).split('\n')
        traceback.reverse()
        return ExceptionResponseSchema(
            exception=exception.__class__.__name__,
            exception_traceback=traceback
        )
