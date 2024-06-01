from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from depends import user_repository
from schemas import OperationStatusResponseSchema
from schemas import UserRequestSchema
from utils import CommonUtils
from utils import ExceptionFactory


async def register_user(user_data: UserRequestSchema, session: AsyncSession) -> OperationStatusResponseSchema:
    """
    Регистрация пользователя.

    :param user_data: Данные пользователя.
    :param session: Сессия БД.
    :return: Информация об операции создания пользователя.
    """
    try:
        user_data.password = await CommonUtils.get_password_hash(user_data.password)
        await user_repository.create(db=session, obj_in=user_data)
        return OperationStatusResponseSchema(status=True, message='The operation was successful')
    except IntegrityError as e:
        raise await ExceptionFactory.get_400_exception(message=f'Bad request: {e.orig}')
    except Exception as e:
        raise await ExceptionFactory.get_500_exception(message=f'Internal server error: {e}')
