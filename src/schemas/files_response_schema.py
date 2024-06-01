from typing import List

from pydantic import BaseModel, Field

from schemas import FileFullSchema


class FilesResponseSchema(BaseModel):
    """
    Модель ответа с информацией о файлах.
    """
    account_id: int = Field(description='Идентификатор пользователя', example=1)
    files: List[FileFullSchema] = Field(
        description='Список файлов',
        example=[
            {
                'id': 1,
                'name': 'notes.txt',
                'created_at': '2020-01-01 00:00:00',
                'path': '/path/to/file.txt',
                'size': 8512,
                'is_downloadable': True
            }
        ]
    )
