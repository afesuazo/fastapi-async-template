from typing import Optional, List

from fastapi import Depends
from sqlalchemy import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.auth_utils import get_hashed_password
from app.crud.base import BaseCRUD
from app.dependencies.db import get_db
from app.models.user import User, UserCreate, UserUpdate


class UserCRUD(BaseCRUD[User, UserCreate, UserUpdate]):
    def __init__(self, db_session: AsyncSession = Depends(get_db)):
        self.db_session = db_session

    async def create(self, user_data: UserCreate) -> User:
        user_data.first_name = user_data.first_name.title()
        user_data.last_name = user_data.last_name.title()
        user_dict = user_data.dict()
        user = User(**user_dict)

        user.hashed_password = get_hashed_password(user_data.password)

        self.db_session.add(user)
        await self.db_session.commit()
        await self.db_session.refresh(user)

        return user

    async def read(self, unique_id: int) -> Optional[User]:
        statement = select(User).where(User.uid == unique_id)
        results = await self.db_session.execute(statement=statement)

        # Scalar one or none allows empty results
        user = results.scalar_one_or_none()
        return user

    async def read_by_username(self, username: str) -> Optional[User]:
        statement = select(User).where(User.username == username)
        results = await self.db_session.execute(statement=statement)

        # Scalar one or none allows empty results
        user = results.scalar_one_or_none()
        return user

    async def read_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        results = await self.db_session.execute(statement=statement)

        # Scalar one or none allows empty results
        user = results.scalar_one_or_none()
        return user

    async def read_many(self, offset: int, limit: int, group_id: Optional[int] = None) -> List[User]:
        statement = select(User).offset(offset).limit(limit)
        results = await self.db_session.execute(statement=statement)

        users = [r for r, in results.all()]
        return users

    async def update(self, unique_id: int, user_data: UserUpdate) -> User:
        user = await self.read(unique_id=unique_id)
        assert user is not None, f"User {unique_id} not found"
        values = user_data.dict()

        for k, v in values.items():
            setattr(user, k, v)

        self.db_session.add(user)
        await self.db_session.commit()
        await self.db_session.refresh(user)

        return user

    async def delete(self, unique_id: int) -> None:
        statement = delete(User).where(User.uid == unique_id)

        await self.db_session.execute(statement=statement)
        await self.db_session.commit()
