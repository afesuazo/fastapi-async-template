import config

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel  # noqa  # Imported here to gather model metadata

DATABASE_URL = config.DB_URL


class AppDB:
    def __init__(self) -> None:
        self.engine: AsyncEngine = create_async_engine(DATABASE_URL)
        self.async_session: sessionmaker[AsyncSession] = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def initiate_db(self) -> None:
        async with self.engine.begin() as conn:
            # This will drop and create all tables at startup
            await conn.run_sync(SQLModel.metadata.drop_all)
            await conn.run_sync(SQLModel.metadata.create_all)