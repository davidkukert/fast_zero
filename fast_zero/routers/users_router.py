from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from fast_zero.db import T_Session
from fast_zero.models import User
from fast_zero.schemas import (
    Message,
    UserDetails,
    UserList,
    UserPublic,
    UserSchema,
)
from fast_zero.security import T_CurrentUser, get_password_hash

users_router = APIRouter(prefix='/users', tags=['users'])


@users_router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
)
def create_user(user: UserSchema, session: T_Session):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email already exists'
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@users_router.get(
    '/',
    response_model=UserList,
)
def read_users(
    session: T_Session,
    limit: int = 10,
    skip: int = 0,
):
    users_list = session.scalars(select(User).limit(limit).offset(skip))
    return {'users': users_list}


@users_router.get(
    '/{user_id}',
    response_model=UserDetails,
)
def read_user(user_id: int, session: T_Session):
    user_data = session.scalar(select(User).where(User.id == user_id))

    if user_data is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return {'user': user_data}


@users_router.put(
    '/{user_id}',
    response_model=UserPublic,
)
def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not permission',
        )

    db_user_conflict = session.scalar(
        select(User).where(
            ((User.username == user.username) | (User.email == user.email))
            & (User.id != user_id)
        )
    )

    if db_user_conflict:
        if db_user_conflict.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif db_user_conflict.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email already exists'
            )

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user


@users_router.delete(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def delete_user(
    user_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not permission',
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted!'}
