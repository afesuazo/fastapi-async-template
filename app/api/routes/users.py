from typing import Optional

from aioredis import Redis
from fastapi import APIRouter, status, Depends, HTTPException, Query

from app.crud.user import UserCRUD
from app.dependencies.redis import get_redis
from app.models.user import UserCreate, User, UserRead

router = APIRouter()


@router.get(
    "/all",
    summary='Get a list of all registered users',
    response_model=list[UserRead]
)
async def get_all_users(
        offset: int = 0,
        limit: int = Query(default=50, lte=50),
        user_crud: UserCRUD = Depends(UserCRUD)
) -> list[User]:
    users = await user_crud.read_many(offset, limit)
    return users


@router.get(
    "/single/{username}",
    summary='Get details of a single user',
    response_model=Optional[UserRead]
)
async def get_single_user(
        username: str,
        user_crud: UserCRUD = Depends(UserCRUD),
        redis: Redis = Depends(get_redis)
) -> Optional[User]:
    user_data = await redis.get(username)
    if user_data:
        return User.parse_raw(user_data)

    # Cache miss
    user = await user_crud.read_by_username(username)
    if user:
        await redis.set(username, user.json())

    return user


@router.post(
    "/register",
    summary="Create a new user",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
        user_data: UserCreate,
        user_crud: UserCRUD = Depends(UserCRUD)
) -> UserRead:
    # Check if already exists
    existing_username = await user_crud.read_by_username(user_data.username)
    if existing_username is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                'msg': "User with this username already exist",
                'field': 'username'
            }
        )
    user_email = await user_crud.read_by_email(user_data.email)
    if user_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                'msg': "User with this email already exist",
                'field': 'email'
            }
        )
    user = await user_crud.create(user_data=user_data)
    user_read = UserRead(**user.dict())
    return user_read
