from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from core import app_settings

engine = create_async_engine(app_settings.DATABASE_DSN, echo=True, future=True)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
