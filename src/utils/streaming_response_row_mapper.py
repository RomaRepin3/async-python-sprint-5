from mimetypes import guess_type
from typing import AsyncIterator

from starlette.responses import StreamingResponse


class StreamingResponseRowMapper:
    """
    Сборка модели ответа StreamResponse.
    """

    @classmethod
    async def _file_iterator(cls, file_object) -> AsyncIterator:
        """
        Асинхронный итератор для файла.

        :param file_object: Объект файла.
        :return: Асинхронный итератор.
        """
        async for chunk in file_object['Body']:
            yield chunk

    @classmethod
    async def map(cls, file_name: str, file_object) -> StreamingResponse:
        """
        Сборка модели ответа StreamResponse.

        :param file_name: Имя файла.
        :param file_object: Объект файла.
        :return: Модель ответа StreamingResponse.
        """
        return StreamingResponse(
            content=cls._file_iterator(file_object),
            headers={
                'Content-Disposition': f'attachment; filename=123.{file_name[file_name.rfind("."):]}',
                'Content-Type': guess_type(file_name)[0]
            }
        )
