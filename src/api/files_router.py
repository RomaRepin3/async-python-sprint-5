from http import HTTPStatus
from typing import Annotated

from aiobotocore.client import AioBaseClient
from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Query
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from depends import get_db_session
from depends import s3_client_dependency
from depends import verify_token
from handlers import download_file
from handlers import get_files_info
from handlers import upload_file
from schemas import FileFullSchema
from schemas import FileUploadRequestSchema

files_router = APIRouter(
    tags=[
        'Files',
    ]
)


@files_router.get(
    '/files/',
    response_model=None,
    status_code=HTTPStatus.OK,
    name='Информация о загруженных файлах'
)
async def get_files(
        user_id: Annotated[int, Depends(verify_token)],
        session: Annotated[AsyncSession, Depends(get_db_session)]
):
    return await get_files_info(user_id=user_id, session=session)


@files_router.post(
    '/files/upload',
    response_model=FileFullSchema,
    status_code=HTTPStatus.CREATED,
    name='Загрузить файл в хранилище'
)
async def upload(
        user_id: Annotated[int, Depends(verify_token)],
        upload_data: Annotated[FileUploadRequestSchema, Depends()],
        file: Annotated[UploadFile, File()],
        session: Annotated[AsyncSession, Depends(get_db_session)],
        s3_client: Annotated[AioBaseClient, Depends(s3_client_dependency)]
) -> FileFullSchema:
    return await upload_file(user_id, upload_data, file, session, s3_client)


@files_router.get(
    '/files/download',
    response_model=None,
    status_code=HTTPStatus.OK,
    name='Скачать загруженный файл'
)
async def download(
        user_id: Annotated[int, Depends(verify_token)],
        session: Annotated[AsyncSession, Depends(get_db_session)],
        s3_client: Annotated[AioBaseClient, Depends(s3_client_dependency)],
        path: str = Query(
            description='Путь к файлу или идентификатор загруженного файла в БД',
            min_length=1
        )
) -> StreamingResponse:
    return await download_file(path, user_id, session, s3_client)
