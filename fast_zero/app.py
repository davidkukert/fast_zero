from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.routers.auth_router import auth_router
from fast_zero.routers.todo_router import todo_router
from fast_zero.routers.users_router import users_router
from fast_zero.schemas import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá, mundo!'}


app.include_router(users_router)
app.include_router(auth_router)
app.include_router(todo_router)
