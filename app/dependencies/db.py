from typing import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Yields db sessions, used by FastApi "Depends"
    """
    async with request.app.state.DB.async_session() as session:
        yield session
