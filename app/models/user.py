from typing import Optional

from sqlmodel import Field, SQLModel


# Data only model
class UserBase(SQLModel):
    email: str = Field(unique=True)
    username: str = Field(unique=True)
    first_name: str
    last_name: str


class User(UserBase, table=True):
    __tablename__ = "user"

    uid: Optional[int] = Field(default=None, primary_key=True, index=True)
    is_active: bool = Field(default=True)
    internal_field: str


# Created to differentiate from Base in docs

class UserCreate(UserBase):
    ...


class UserUpdate(UserBase):
    ...


class UserRead(UserBase):
    is_active: bool
