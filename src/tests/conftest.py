from typing import Dict

from faker import Faker
from httpx import AsyncClient
from pytest import fixture

from db import async_session
from depends import get_db_session
from main import app

fake = Faker()


@fixture
async def db_fixture():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


@fixture
async def client(db_fixture) -> AsyncClient:
    async def override_get_db():
        yield db_fixture

    app.dependency_overrides[get_db_session] = override_get_db  # noqa
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


@fixture
def user_data() -> Dict[str, str]:
    return {
        'login': fake.user_name(),
        'password': fake.user_name()
    }
