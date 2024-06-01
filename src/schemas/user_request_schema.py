from pydantic import BaseModel, Field


class UserRequestSchema(BaseModel):
    """
    Модель для передачи данных пользователя.
    """
    login: str = Field(
        description='Логин пользователя',
        max_length=100,
        min_length=5,
        example='user_name'
    )
    password: str = Field(
        description='Пароль пользователя',
        max_length=100,
        min_length=5,
        example='user_password'
    )
