from pytest import mark

from utils import CommonUtils


class TestCommonUtils:

    @mark.asyncio
    async def test_get_password_hash(self, user_data):
        password_hash = await CommonUtils.get_password_hash(user_data['password'])
        assert isinstance(password_hash, str), f'Expected str, got {type(password_hash)}'
        assert password_hash, f'Expected not empty, got {password_hash}'

    @mark.asyncio
    async def test_verify_password(self, user_data):
        password_hash = await CommonUtils.get_password_hash(user_data['password'])
        assert CommonUtils.verify_password(user_data['password'], password_hash), f'Expected True, got False'

    @mark.asyncio
    async def test_create_access_token(self, user_data):
        token = await CommonUtils.create_access_token(user_data)
        assert isinstance(token, str), f'Expected str, got {type(token)}'
        assert token, f'Expected not empty, got {token}'
