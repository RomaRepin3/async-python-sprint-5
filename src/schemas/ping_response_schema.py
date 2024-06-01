from pydantic import BaseModel, Field


class PingResponseSchema(BaseModel):
    """
    Модель ответа пинга.
    """
    db: float = Field(description='Время доступа к БД', example=1.27)
    redis: float = Field(description='Время доступа к Redis', example=1.89)
    s3: float = Field(description='Время доступа к S3', example=0.56)
