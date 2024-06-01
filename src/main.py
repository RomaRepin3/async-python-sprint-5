from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.responses import ORJSONResponse

from api import auth_router
from api import files_router
from api import system_router
from core import app_settings
from depends import get_s3_client
from utils import JsonResponseRowMapper


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    async with await get_s3_client() as s3_client:
        await s3_client.create_bucket(Bucket=app_settings.S3_BUCKET)
        await s3_client.close()
    yield

app = FastAPI(
    title=app_settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)
app.include_router(auth_router, prefix='/api')
app.include_router(files_router, prefix='/api')
app.include_router(system_router, prefix='/api')


@app.exception_handler(HTTPException)
async def handle_http_exception(request: Request, exception: HTTPException) -> JSONResponse:  # noqa
    return await JsonResponseRowMapper.get_from_http_exception(exception=exception)


@app.exception_handler(Exception)
async def handle_exception(request: Request, exception: Exception) -> JSONResponse:  # noqa
    return await JsonResponseRowMapper.get_from_exception(exception=exception)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=app_settings.PROJECT_HOST,
        port=app_settings.PROJECT_PORT,
    )
