from pydantic import BaseModel
from pydantic import Field


class OperationStatusResponseSchema(BaseModel):
    """
    Модель ответа на операцию.
    """
    status: bool = Field(
        description='Статус операции',
        example='true',
        default=True
    )
    message: str = Field(
        description='Сообщение об операции',
        example='The operation was successful',
        default='The operation was successful'
    )
