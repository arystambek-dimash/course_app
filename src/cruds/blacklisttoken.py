from typing import Optional

from sqlalchemy import select, insert, String

import src.db.schemas.tokens as tokens_schema
from src.db.database import async_session
from src.db.models.blacklisttoken import BlacklistToken


class BlacklistTokenCRUD:
    @staticmethod
    async def get_token(refresh_token: str) -> Optional[tokens_schema.RefreshToken]:
        async with async_session() as session:
            query = select(BlacklistToken).where(BlacklistToken.refresh_token.cast(String) == refresh_token)
            result = await session.execute(query)
            db_token = result.scalar_one_or_none()
            return tokens_schema.RefreshToken(refresh_token=db_token.refresh_token) if db_token else None

    @staticmethod
    async def create_token(refresh_token: str) -> None:
        async with async_session() as session:
            query = insert(BlacklistToken).values(refresh_token=refresh_token)
            result = await session.execute(query)
            await session.commit()
        return result
