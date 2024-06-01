from datetime import datetime

from pytest import mark

from models import FileModel
from schemas import FilesResponseSchema
from utils import FileFullSchemaRowMapper
from utils import FilesResponseSchemaRowMapper


class TestFilesResponseSchemaRowMapper:
    @mark.asyncio
    async def test_map(self):
        """
        Преобразование модели FileModel в модель FilesResponseSchema.
        """

        file_models = [
            FileModel(
                id=1,
                name='test',
                created_at=datetime.now(),
                path='test',
                size=1,
                is_downloadable=True
            ),
            FileModel(
                id=2,
                name='test',
                created_at=datetime.now(),
                path='test',
                size=1,
                is_downloadable=True
            ),
        ]

        assert await FilesResponseSchemaRowMapper.map(1, file_models) == FilesResponseSchema(
            account_id=1,
            files=[
                await FileFullSchemaRowMapper.map(file_model) for file_model in file_models
            ]
        )
