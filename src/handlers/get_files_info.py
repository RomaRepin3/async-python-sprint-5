from sqlalchemy.ext.asyncio import AsyncSession

from depends import file_repository
from schemas import FilesResponseSchema
from utils import FilesResponseSchemaRowMapper


async def get_files_info(user_id: int, session: AsyncSession) -> FilesResponseSchema:
    """
    Получение информации о файлах.

    :param user_id: Идентификатор пользователя.
    :param session: Сессия БД.
    :return: Модель FilesResponseSchema.
    """
    files_models = await file_repository.get_by_user_id(db=session, user_id=user_id)

    return await FilesResponseSchemaRowMapper.map(user_id=user_id, files_models=files_models)
