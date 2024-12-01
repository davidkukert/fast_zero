from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from fast_zero.models import TodoState


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDb(UserSchema):
    id: int


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(
        from_attributes=True,
    )


class UserList(BaseModel):
    users: list[UserPublic]


class UserDetails(BaseModel):
    user: UserPublic


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoPublic(TodoSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class TodoList(BaseModel):
    todos: list[TodoPublic]


class FilterPage(BaseModel):
    limit: int | None = None
    offset: int | None = None


class FilterTodo(FilterPage):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None
