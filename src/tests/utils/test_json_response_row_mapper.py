from fastapi import HTTPException
from fastapi import status
from pytest import mark

from utils import JsonResponseRowMapper


class TestJsonResponseRowMapper:
    @mark.asyncio
    async def test_get_from_http_exception(self):
        """
        Возвращает JSON ответ с сообщением об ошибке для HTTP исключения.
        """

        exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
        result = await JsonResponseRowMapper.get_from_http_exception(exception=exception)
        assert result.status_code == status.HTTP_404_NOT_FOUND
        assert result.body == b'{"exception":"Not found","exception_traceback":[]}'

    @mark.asyncio
    async def test_get_from_exception(self):
        """
        Возвращает JSON ответ с сообщением об ошибке для внештатного исключения.
        """

        exception = Exception('test')
        result = await JsonResponseRowMapper.get_from_exception(exception=exception)
        assert result.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert result.body == b'{"exception":"Exception","exception_traceback":["","NoneType: None"]}'
