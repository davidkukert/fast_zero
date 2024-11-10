from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from fast_zero.db import T_Session
from fast_zero.models import User
from fast_zero.schemas import Token
from fast_zero.security import (
    T_CurrentUser,
    create_access_token,
    verify_password,
)

auth_router = APIRouter(prefix='/auth', tags=['auth'])
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@auth_router.post('/token', response_model=Token)
def login_for_access_token(
    session: T_Session,
    form_data: T_OAuth2Form,
):
    user = session.scalar(
        select(User).where(User.username == form_data.username)
    )

    if user is None or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
        )

    access_token = create_access_token(data={'sub': user.username})

    return {'access_token': access_token, 'token_type': 'Bearer'}


@auth_router.post('/refresh_token', response_model=Token)
def refresh_access_token(
    user: T_CurrentUser,
):
    new_access_token = create_access_token(data={'sub': user.username})

    return {'access_token': new_access_token, 'token_type': 'bearer'}
