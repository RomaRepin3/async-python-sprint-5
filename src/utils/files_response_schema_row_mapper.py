from typing import List

from models import FileModel
from schemas import FilesResponseSchema

from .file_full_schema_row_mapper import FileFullSchemaRowMapper


class FilesResponseSchemaRowMapper:
    """
    Сборка модели FilesResponseSchema.
    """

    @staticmethod
    async def map(user_id: int, files_models: List[FileModel]) -> FilesResponseSchema:
        """
        Преобразование модели FileModel в модель FilesResponseSchema.

        :param user_id: Идентификатор пользователя.
        :param files_models: Модели файлов.
        :return: Модель FilesResponseSchema.
        """
        files = list()
        for file_model in files_models:
            files.append(await FileFullSchemaRowMapper.map(file_model))
        return FilesResponseSchema(account_id=user_id, files=files)
