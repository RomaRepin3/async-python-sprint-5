from http import HTTPStatus

from fastapi import HTTPException
from pytest import mark

from utils import ExceptionResponseSchemaRowMapper


class TestExceptionResponseSchemaRowMapper:

    @mark.asyncio
    async def test_get_from_http_exception(self):
        exception = HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Bad request')
        schema = await ExceptionResponseSchemaRowMapper.get_from_http_exception(exception)
        assert schema.exception == 'Bad request', f'Expected Bad request, got {schema.exception}'
        assert schema.exception_traceback == [], f'Expected empty list, got {schema.exception_traceback}'

    @mark.asyncio
    async def test_get_from_exception(self):
        exception = ValueError('ValueError')
        schema = await ExceptionResponseSchemaRowMapper.get_from_exception(exception)
        assert schema.exception == 'ValueError', f'Expected ValueError, got {schema.exception}'
        assert schema.exception_traceback, f'Expected not empty list, got {schema.exception_traceback}'
