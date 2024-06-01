from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from .base_model import BaseModel


class FileModel(BaseModel):
    """
    Модель файла.
    """

    __tablename__ = 'file'

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, doc='Идентификатор пользователя')
    name = Column(String(100), nullable=False, doc='Имя файла')
    path = Column(String(500), nullable=False, unique=True, doc='Полный путь к файлу')
    size = Column(Integer, nullable=False, doc='Размер файла в байтах')
    is_downloadable = Column(Boolean, nullable=False, default=True, doc='Файл можно скачивать')
