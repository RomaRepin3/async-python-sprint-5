from pydantic import BaseModel
from pydantic import Field


class FileFullSchema(BaseModel):
    """
    Модель полного файла.
    """
    id: int = Field(description='Идентификатор', example=1)
    name: str = Field(description='Имя файла', example='notes.txt')
    created_at: str = Field(description='Дата создания', example='2020-01-01 00:00:00')
    path: str = Field(description='Путь к файлу', example='path/to/file.txt')
    size: int = Field(description='Размер файла в байтах', example=8512)
    is_downloadable: bool = Field(description='Файл можно скачивать', example=True)
