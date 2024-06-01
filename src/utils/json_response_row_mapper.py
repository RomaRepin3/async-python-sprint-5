from fastapi import HTTPException
from fastapi import status
from fastapi.responses import JSONResponse

from core import app_logger
from .exception_response_schema_row_mapper import ExceptionResponseSchemaRowMapper


class JsonResponseRowMapper:
    """
    Сборка JSON ответа.
    """

    @staticmethod
    async def get_from_http_exception(exception: HTTPException) -> JSONResponse:
        """
        Возвращает JSON ответ с сообщением об ошибке для HTTP исключения.

        :param exception: Объект исключения.
        :return: JSON ответ с сообщением об ошибке.
        """
        app_logger.info(f'Mapping http error json response: {exception.detail}')
        return JSONResponse(
            status_code=exception.status_code,
            content=(await ExceptionResponseSchemaRowMapper.get_from_http_exception(exception=exception)).dict()
        )

    @staticmethod
    async def get_from_exception(exception: Exception) -> JSONResponse:
        """
        Возвращает JSON ответ с сообщением об ошибке для внештатного исключения.

        :param exception: Объект исключения.
        :return: JSON ответ с сообщением об ошибке.
        """
        app_logger.error(f'Mapping unexpected error json response: {exception}')
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=(await ExceptionResponseSchemaRowMapper.get_from_exception(exception=exception)).dict()
        )
