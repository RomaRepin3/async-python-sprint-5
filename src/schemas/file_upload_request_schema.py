from pydantic import BaseModel
from pydantic import Field


class FileUploadRequestSchema(BaseModel):
    """
    Модель запроса на загрузку файла.
    """
    path: str = Field(
        description='Полный путь к файлу или к директории, если передан путь к директории, то имя файла будет таким же '
                    'как у передаваемого файла',
        example='/path/to/file.txt',
        max_length=500,
        min_length=2
    )
