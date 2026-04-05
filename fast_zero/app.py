from http import HTTPStatus
from fastapi import FastAPI
from fast_zero.schemas import Message # Importando o Schema

app = FastAPI()

@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'Adriano': 'Olá Mundo!'}