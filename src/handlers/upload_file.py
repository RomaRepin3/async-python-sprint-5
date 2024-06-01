from aiobotocore.client import AioBaseClient
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from depends import file_repository
from repositories import S3Repository
from schemas import FileFullSchema
from schemas import FileUploadRequestSchema
from utils import FileCreateSchemaRowMapper
from utils import FileFullSchemaRowMapper


async def upload_file(
        user_id: int,
        upload_data: FileUploadRequestSchema,
        file: UploadFile,
        session: AsyncSession,
        s3_client: AioBaseClient
) -> FileFullSchema:
    """
    Загрузка файла в хранилище.

    :param user_id: Идентификатор пользователя.
    :param upload_data: Данные запроса.
    :param file: Файл.
    :param session: Сессия БД.
    :param s3_client: Клиент S3.
    :return: Данные загруженного файла.
    """
    # Формирование имени файла и полного пути к нему
    last_path_part = upload_data.path.split('/')[-1]
    file_name = last_path_part if '.' in last_path_part else file.filename
    if '.' not in last_path_part:
        upload_data.path = f'{upload_data.path}/{file_name}'

    # Проверка присутствия файла в БД
    file_model = await file_repository.get_by_path(db=session, path=upload_data.path)

    # Создание записи в БД при отсутствии
    if not file_model:
        file_model = await file_repository.create(
            db=session,
            obj_in=await FileCreateSchemaRowMapper.map(
                user_id=user_id,
                name=file_name,
                upload_data=upload_data,
                file=file
            )
        )

    # Загрузка файла в хранилище
    await S3Repository.create(s3_client=s3_client, key=upload_data.path, file_object=file.file)

    return await FileFullSchemaRowMapper.map(file_model)
