from http import HTTPStatus
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from fast_zero.database import get_session, create_db
from fast_zero.models import User
from fast_zero.schemas import UserPublic, UserSchema
from typing import List

app = FastAPI()

# Comando para criar as tabelas ao subir a aplicação
@app.on_event("startup")
def on_startup():
    create_db()

@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    # Verifica se o e-mail já existe no banco real
    db_user = session.scalar(select(User).where(User.email == user.email))
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user

@app.get('/users/', response_model=List[UserPublic])
def list_users(session: Session = Depends(get_session)):
    # 1. Busca todos os usuários na tabela 'User'
    users = session.scalars(select(User)).all()
    
    # 2. Retorna a lista (o FastAPI + Pydantic cuidam da conversão verifica Deploy)
    return users    

import os  # Adicione este import
from http import HTTPStatus
from fastapi import FastAPI, Depends, HTTPException
# ... (seus outros imports)

app = FastAPI()

@app.get('/')
def read_root():
    # Coleta as variáveis que vamos injetar via Stack/Docker
    return {
        "projeto": "Inetz Lab",
        "aluno_id": os.getenv("ALUNO_NUM", "Não definido"),
        "repositorio": os.getenv("GITHUB_REPO", "Não definido"),
        "ambiente": "Docker Swarm",
        "status": "Online e Integrado"
    }

# ... (restante do seu código de usuários)    