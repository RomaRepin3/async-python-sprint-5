from datetime import datetime

from pytest import mark

from models import FileModel
from schemas import FileFullSchema
from utils import FileFullSchemaRowMapper


class TestFileFullSchemaRowMapper:
    @mark.asyncio
    async def test_map(self):
        """
        Преобразование модели FileModel в модель FileFullSchema.
        """

        file_model = FileModel(
            id=1,
            name='test',
            created_at=datetime.now(),
            path='test',
            size=1,
            is_downloadable=True
        )

        assert await FileFullSchemaRowMapper.map(file_model) == FileFullSchema(
            id=file_model.id,
            name=file_model.name,
            created_at=file_model.created_at.isoformat(),
            path=file_model.path,
            size=file_model.size,
            is_downloadable=file_model.is_downloadable
        )
