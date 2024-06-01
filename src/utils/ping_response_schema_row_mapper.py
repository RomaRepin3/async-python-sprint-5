from schemas import PingResponseSchema


class PingResponseSchemaRowMapper:
    """
    Сборка модели PingResponseSchema.
    """

    @staticmethod
    async def map(db_ping: float, redis_ping: float, s3_ping: float) -> PingResponseSchema:
        """
        Сборка модели PingResponseSchema.

        :param db_ping: Пинг БД.
        :param redis_ping: Пинг Redis.
        :param s3_ping: Пинг S3.
        :return: Модель PingResponseSchema.
        """
        return PingResponseSchema(db=db_ping, redis=redis_ping, s3=s3_ping)
