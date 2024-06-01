from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    """
    Модель токена.
    """
    access_token: str = Field(
        description='Токен доступа',
        example='eyJhbGciOiJIUzI1Ni.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0.SflKxwRJSMeKKF2QT4fwpMeJf'
    )
    token_type: str = Field(
        description='Тип токена',
        example='bearer',
        default='bearer'
    )
