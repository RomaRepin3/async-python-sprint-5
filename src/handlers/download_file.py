from aiobotocore.client import AioBaseClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from depends import file_repository
from models import FileModel
from repositories import S3Repository
from utils import ExceptionFactory
from utils import StreamingResponseRowMapper


async def download_file(
        file_path_or_id: str,
        user_id: int,
        session: AsyncSession,
        s3_client: AioBaseClient
) -> StreamingResponse:
    """
    Скачивание файла.

    :param file_path_or_id: Полный путь к файлу или его идентификатор.
    :param user_id:
    :param session:
    :param s3_client:
    :return:
    """

    file_path: str
    file_model: FileModel
    if file_path_or_id.isdigit():
        file_model = await file_repository.get_by_id_and_user_id(
            db=session,
            file_id=int(file_path_or_id),
            user_id=user_id
        )
        file_path = file_model.path if file_model else ''
    else:
        file_model = await file_repository.get_by_path_and_user_id(
            db=session,
            user_id=user_id,
            path=file_path_or_id
        )
        file_path = file_path_or_id if file_model else ''
    if not file_path:
        raise await ExceptionFactory.get_404_exception(f'File not found: {file_path_or_id}')

    file_object = await S3Repository.get(s3_client=s3_client, key=file_path)
    if not file_object:
        raise await ExceptionFactory.get_500_exception(f'File record found in DB, but file not found: {file_model}')

    return await StreamingResponseRowMapper.map(file_name=file_model.name, file_object=file_object)
