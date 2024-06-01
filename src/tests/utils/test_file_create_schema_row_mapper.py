from typing import BinaryIO

from fastapi import UploadFile
from pytest import mark

from schemas import FileUploadRequestSchema
from utils import FileCreateSchemaRowMapper


class TestFileCreateSchemaRowMapper:

    @mark.asyncio
    async def test_map(self):
        name = 'test.txt'
        user_id = 1
        upload_data = FileUploadRequestSchema(path='test')
        file = UploadFile(filename='test', file=BinaryIO(), size=4)
        schema = await FileCreateSchemaRowMapper.map(name, user_id, upload_data, file)
        assert schema.name == name, f'Expected {name}, got {schema.name}'
        assert schema.user_id == user_id, f'Expected {user_id}, got {schema.user_id}'
        assert schema.path == upload_data.path, f'Expected {upload_data.path}, got {schema.path}'
        assert schema.size == file.size, f'Expected {file.size}, got {schema.size}'
        assert schema.is_downloadable, f'Expected True, got {schema.is_downloadable}'
