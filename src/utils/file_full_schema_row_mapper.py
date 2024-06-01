from models import FileModel
from schemas import FileFullSchema


class FileFullSchemaRowMapper:
    """
    Сборка модели FileFullSchema.
    """

    @staticmethod
    async def map(file_model: FileModel):
        """
        Преобразование модели FileModel в модель FileFullSchema.

        :param file_model: Модель FileModel.
        :return: Модель FileFullSchema.
        """

        return FileFullSchema(
            id=file_model.id,
            name=file_model.name,
            created_at=file_model.created_at.isoformat(),
            path=file_model.path,
            size=file_model.size,
            is_downloadable=file_model.is_downloadable
        )
