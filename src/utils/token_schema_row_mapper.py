from schemas import TokenSchema


class TokenSchemaRowMapper:
    """
    Маппер для схемы токена.
    """

    @staticmethod
    async def get_token_schema(token: str) -> TokenSchema:
        """
        Маппер схемы токена.

        :param token: Токен.
        :return: Схема токена.
        """
        return TokenSchema(access_token=token, token_type='bearer')
