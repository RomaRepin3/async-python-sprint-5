from pydantic import BaseModel
from pydantic import Field


class FileCreateSchema(BaseModel):
    """
    Схема создания файла.
    """

    user_id: int = Field(
        description='Идентификатор пользователя',
        example=1,
        gt=0
    )
    name: str = Field(
        description='Имя файла',
        max_length=100,
        example='notes.txt'
    )
    path: str = Field(
        description='Полный путь к файлу',
        example='/homework/test-fodler/notes.txt',
        max_length=500,
        min_length=2
    )
    size: int = Field(
        description='Размер файла в байтах',
        example=8512
    )
    is_downloadable: bool = Field(
        description='Файл можно скачивать',
        example=True,
        default=True
    )
