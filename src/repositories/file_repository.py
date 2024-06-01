from typing import List
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import FileModel
from schemas import FileCreateSchema
from .repository_db import RepositoryDB


class FileRepository(RepositoryDB[FileModel, FileCreateSchema, FileCreateSchema]):
    """
    Репозиторий для работы с файлами.
    """

    async def get_by_path(self, db: AsyncSession, *, path: str) -> Optional[FileModel]:
        """
        Поиск файла по пути.

        :param db: Сессия БД.
        :param path: Полный путь к файлу.
        :return: Файл.
        """
        statement = select(self._model).where(self._model.path == path)  # type: ignore
        result = await db.execute(statement=statement)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, db: AsyncSession, *, user_id: int) -> List[FileModel]:
        """
        Получение списка файлов пользователя.

        :param db: Сессия БД.
        :param user_id: Идентификатор пользователя.
        :return: Список файлов.
        """
        statement = select(self._model).where(self._model.user_id == user_id)  # type: ignore
        result = await db.execute(statement=statement)
        return list(result.scalars().all())

    async def get_by_id_and_user_id(self, db: AsyncSession, file_id: int, user_id: int) -> Optional[FileModel]:
        """
        Поиск файла по идентификатору и идентификатору пользователя.

        :param db: Сессия БД.
        :param file_id: Идентификатор файла.
        :param user_id: Идентификатор пользователя.
        :return: Файл.
        """
        statement = select(self._model).where(self._model.id == file_id, self._model.user_id == user_id)  # type: ignore
        result = await db.execute(statement=statement)
        return result.scalar_one_or_none()

    async def get_by_path_and_user_id(self, db: AsyncSession, user_id: int, path: str) -> Optional[FileModel]:
        """
        Поиск файла по пути и идентификатору пользователя.

        :param db: Сессия БД.
        :param user_id: Идентификатор пользователя.
        :param path: Полный путь к файлу.
        :return: Файл.
        """
        statement = select(self._model).where(self._model.user_id == user_id, self._model.path == path)  # type: ignore
        result = await db.execute(statement=statement)
        return result.scalar_one_or_none()
