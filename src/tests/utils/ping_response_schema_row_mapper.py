from pytest import mark

from schemas import PingResponseSchema
from utils import PingResponseSchemaRowMapper


class TestPingResponseSchemaRowMapper:

    @mark.asyncio
    async def test_map(self):
        """
        Преобразование модели PingResponse в модель PingResponseSchema.
        """
        result = await PingResponseSchemaRowMapper.map(db_ping=3.5, redis_ping=2.3, s3_ping=1.2)
        assert result == PingResponseSchema(db=3.5, redis=2.3, s3=1.2)
