from sqlalchemy import Column
from sqlalchemy import String

from .base_model import BaseModel


class UserModel(BaseModel):
    """
    Модель пользователя.
    """
    __tablename__ = 'user'

    login = Column(String(100), unique=True, nullable=False, doc='Логин пользователя')
    password = Column(String(100), nullable=False, doc='Пароль пользователя')
