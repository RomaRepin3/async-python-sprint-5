from typing import List

from pydantic import BaseModel
from pydantic import Field


class ExceptionResponseSchema(BaseModel):
    """
    Сборка модели ответа исключения.
    """

    exception: str = Field(description='Класс исключения', example='ValueError')
    exception_traceback: List[str] = Field(description='Трассировка исключения', example='ValueError')
