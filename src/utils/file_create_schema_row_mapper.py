from fastapi import UploadFile

from schemas import FileCreateSchema
from schemas import FileUploadRequestSchema


class FileCreateSchemaRowMapper:
    """
    Сборка модели FileCreateSchema.
    """

    @staticmethod
    async def map(name: str, user_id: int, upload_data: FileUploadRequestSchema, file: UploadFile) -> FileCreateSchema:
        """
        Сборка модели FileCreateSchema.

        :param user_id: Идентификатор пользователя.
        :param name: Имя файла.
        :param upload_data: Данные запроса.
        :param file: Файл.
        :return: Модель FileCreateSchema.
        """
        return FileCreateSchema(
            user_id=user_id,
            name=name,
            path=upload_data.path,
            size=file.size,
            is_downloadable=True
        )
