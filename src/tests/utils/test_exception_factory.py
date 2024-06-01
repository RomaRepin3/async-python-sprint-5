from http import HTTPStatus

from pytest import mark

from utils import ExceptionFactory


class TestExceptionFactory:

    @mark.asyncio
    async def test_get_400_exception(self):
        message = 'Bad request'
        http_exception = await ExceptionFactory.get_400_exception(message)
        assert http_exception.status_code == HTTPStatus.BAD_REQUEST
        assert http_exception.detail == message

    @mark.asyncio
    async def test_get_401_exception(self):
        message = 'Unauthorized'
        http_exception = await ExceptionFactory.get_401_exception(message)
        assert http_exception.status_code == HTTPStatus.UNAUTHORIZED
        assert http_exception.headers['WWW-Authenticate'] == 'Bearer'
        assert http_exception.detail == message

    @mark.asyncio
    async def test_get_404_exception(self):
        message = 'Not found'
        http_exception = await ExceptionFactory.get_404_exception(message)
        assert http_exception.status_code == HTTPStatus.NOT_FOUND
        assert http_exception.detail == message

    @mark.asyncio
    async def test_get_500_exception(self):
        message = 'Internal server error'
        http_exception = await ExceptionFactory.get_500_exception(message)
        assert http_exception.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert http_exception.detail == message
