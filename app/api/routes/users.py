from datetime import timedelta
from typing import Optional, List

from aioredis import Redis
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from pydantic import BaseModel

from app.api.auth_utils import verify_password, create_access_token
from app.api.cypt_utils import generate_master_key
from app.crud.user import UserCRUD
from app.dependencies.auth import get_current_user
from app.dependencies.redis import get_redis
from app.models.user import UserCreate, User, UserRead
from config import ACCESS_TOKEN_EXPIRE_MINUTES, SALT_1

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str
    expiration_time: int


async def authenticate_user(username: str, password: str, user_crud: UserCRUD) -> Optional[User]:
    user: Optional[User] = await (user_crud.read_by_username(username=username))
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


@router.get("/all-users")
async def temp_users(user_crud: UserCRUD = Depends(UserCRUD)) -> list[User]:
    users = await user_crud.read_many(0, 100)
    return users


@router.post(
    "/login",
    summary="Login user and assign token",
    status_code=status.HTTP_200_OK
)
async def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        user_crud: UserCRUD = Depends(UserCRUD),
        redis: Redis = Depends(get_redis)
):
    user: Optional[User] = await authenticate_user(form_data.username, form_data.password, user_crud)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                'msg': "Incorrect username & password combination",
            }
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    crypt_key = generate_master_key(form_data.password + SALT_1.decode())
    await redis.execute_command('set', str(user.uid), crypt_key, 'ex', ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    token = Token(access_token=access_token, token_type="bearer", expiration_time=access_token_expires.seconds)

    response = {
        **user.dict(),
        **token.dict()
    }

    # Return user details and token
    return response


@router.post(
    "/signup",
    summary="Create new user",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED
)
async def signup_user(
        user_data: UserCreate, user_crud: UserCRUD = Depends(UserCRUD)
) -> UserRead:
    user_username = await user_crud.read_by_username(user_data.username)
    if user_username is not None:
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


@router.get(
    "/me",
    summary='Get details of currently logged in user',
    response_model=User
)
async def get_me(
        user: User = Depends(get_current_user)
) -> User:
    return user
