from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core import app_logger
from models import UserModel
from schemas import UserRequestSchema
from .repository_db import RepositoryDB


class UserRepository(RepositoryDB[UserModel, UserRequestSchema, None]):
    """
    Репозиторий для работы с пользователями.
    """

    async def get_by_login(self, db: AsyncSession, *, login: str) -> Optional[UserModel]:
        """
        Поиск пользователя по логину.

        :param db: Сессия БД.
        :param login: Логин пользователя.
        :return: Пользователь.
        """
        app_logger.info(f'Find user by login: {login}')
        statement = select(self._model).where(self._model.login == login)  # type: ignore
        result = await db.execute(statement=statement)
        app_logger.info(f'Result: {result}')
        return result.scalar_one_or_none()
