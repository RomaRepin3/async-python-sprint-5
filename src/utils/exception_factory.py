from http import HTTPStatus

from fastapi import HTTPException

from core.config import app_logger


class ExceptionFactory:
    """
    Фабрика исключений.
    """

    @staticmethod
    async def get_400_exception(message: str) -> HTTPException:
        """
        Фабрика исключений 400.

        :param message: Сообщение об ошибке.
        :return: Исключение 400.
        """
        app_logger.exception(f'Bad request: {message}')
        return HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=message)

    @staticmethod
    async def get_401_exception(message: str) -> HTTPException:
        """
        Фабрика исключений 401.

        :param message: Сообщение об ошибке.
        :return: Исключение 401.
        """
        app_logger.exception(f'Unauthorized: {message}')
        return HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            headers={
                'WWW-Authenticate': 'Bearer',
            },
            detail=message
        )

    @staticmethod
    async def get_404_exception(message: str) -> HTTPException:
        """
        Фабрика исключений 404.

        :param message: Сообщение об ошибке.
        :return: Исключение 404.
        """
        app_logger.exception(f'Not found: {message}')
        return HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=message)

    @staticmethod
    async def get_500_exception(message: str) -> HTTPException:
        """
        Фабрика исключений 500.

        :param message: Сообщение об ошибке.
        :return: Исключение 500.
        """
        app_logger.exception(f'Internal server error: {message}')
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=message)
