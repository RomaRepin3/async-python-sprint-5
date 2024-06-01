from typing import Any
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from core import app_logger
from models.base import Base
from .base_repository import BaseRepository

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class RepositoryDB(BaseRepository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self._model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        app_logger.info(f'Getting object by id: {id}')
        statement = select(self._model).where(self._model.id == id)  # noqa
        results = await db.execute(statement=statement)
        app_logger.info('Get object by id is OK!')
        return results.scalar_one_or_none()

    async def get_multi(self, db: AsyncSession, *, skip=0, limit=100) -> List[ModelType]:
        app_logger.info(f'Getting objects: skip={skip}, limit={limit}')
        statement = select(self._model).offset(skip).limit(limit)
        results = await db.execute(statement=statement)
        app_logger.info('Get objects is OK!')
        return list(results.scalars().all())

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        app_logger.info(f'Creating object: {obj_in}')
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self._model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        app_logger.info('Create object is OK!')
        return db_obj

    async def update(
            self,
            db: AsyncSession,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        app_logger.info(f'Updating object: {obj_in}')
        obj_update_data = jsonable_encoder(obj_in)
        obj_update_data['id'] = db_obj.id
        obj_update_data['created_at'] = db_obj.created_at
        # db_obj = self._model(id=db_obj.id, created_at=db_obj.created_at, **obj_update_data)
        # db.add(db_obj)
        statement = update(self._model).values(**obj_update_data)
        await db.execute(statement=statement)
        await db.commit()
        await db.refresh(db_obj)
        app_logger.info('Update object is OK!')
        return db_obj

    async def delete(self, db: AsyncSession, *, id: int) -> ModelType:
        app_logger.info(f'Deleting object by id: {id}')
        db_obj = await self.get(db, id)
        if db_obj:
            db_obj.is_deleted = True
            db.add(db_obj)
            await db.commit()
            app_logger.info('Delete object is OK!')
        return db_obj
