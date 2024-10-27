from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.routes.users_routes import users_router
from fast_zero.schemas import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá, mundo!'}


app.include_router(users_router)
