from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import (
    Message,
    UserDb,
    UserDetails,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá, mundo!'}


@app.post(
    '/users',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
    tags=['users'],
)
def create_user(user: UserSchema):
    user_with_id = UserDb(id=len(database) + 1, **user.model_dump())

    database.append(user_with_id)

    return user_with_id


@app.get('/users', response_model=UserList, tags=['users'])
def read_users():
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserPublic, tags=['users'])
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_with_id = UserDb(id=user_id, **user.model_dump())
    database[user_id - 1] = user_with_id
    return user_with_id


@app.get('/users/{user_id}', response_model=UserDetails, tags=['users'])
def read_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return {'user': database[user_id - 1]}


@app.delete(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
    tags=['users'],
)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    del database[user_id - 1]

    return {'message': 'User deleted!'}
