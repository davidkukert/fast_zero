from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from fast_zero.db import SessionDep
from fast_zero.models import User
from fast_zero.schemas import (
    Message,
    UserDetails,
    UserList,
    UserPublic,
    UserSchema,
)

users_router = APIRouter(prefix='/users', tags=['users'])


@users_router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
)
def create_user(user: UserSchema, session: SessionDep):
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
        username=user.username, email=user.email, password=user.password
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
    session: SessionDep,
    limit: int = 10,
    skip: int = 0,
):
    users_list = session.scalars(select(User).limit(limit).offset(skip))
    return {'users': users_list}


@users_router.get(
    '/{user_id}',
    response_model=UserDetails,
)
def read_user(user_id: int, session: SessionDep):
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
def update_user(user_id: int, user: UserSchema, session: SessionDep):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
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

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@users_router.delete(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def delete_user(user_id: int, session: SessionDep):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted!'}
