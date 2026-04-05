from http import HTTPStatus
from fastapi import FastAPI
from fast_zero.schemas import UserPublic, UserSchema, UserDB, Message

app = FastAPI()

# Banco de dados temporário (em memória)
database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'Adriano': 'Olá Mundo!'}

@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    # Simulando a criação de um ID único
    user_with_id = UserDB(
        **user.model_dump(), 
        id=len(database) + 1
    )
    
    database.append(user_with_id)
    
    # O FastAPI filtrará automaticamente a senha, pois usamos UserPublic no response_model
    return user_with_id