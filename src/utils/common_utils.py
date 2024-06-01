from datetime import timedelta
from datetime import datetime
from datetime import timezone
from typing import Union

from jwt import encode

from core import app_settings
from depends import password_context


class CommonUtils:
    """
    Общие утилиты.
    """

    @staticmethod
    async def get_password_hash(password: str) -> str:
        """
        Генерация хэша пароля.

        :param password: Пароль.
        :return: Хэш пароля.
        """
        return password_context.hash(password)

    @staticmethod
    async def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Проверка пароля.

        :param plain_password: Пароль.
        :param hashed_password: Хэш пароля.
        :return: Результат проверки пароля.
        """
        return password_context.verify(plain_password, hashed_password)

    @staticmethod
    async def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = encode(to_encode, app_settings.SECRET_KEY, algorithm=app_settings.ALGORITHM)
        return encoded_jwt
