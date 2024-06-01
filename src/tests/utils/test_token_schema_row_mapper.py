from pytest import mark

from schemas import TokenSchema
from utils import TokenSchemaRowMapper


class TestTokenSchemaRowMappr:

    @mark.asyncio
    async def test_get_token_schema(self):
        token = 'test'
        result = await TokenSchemaRowMapper.get_token_schema(token=token)
        assert result == TokenSchema(access_token=token, token_type='bearer')
