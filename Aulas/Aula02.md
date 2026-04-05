## 📘 Aula-02: CRUD, HTTP e o Contrato de Cadastro

Na aula passada, vimos como o FastAPI funciona. Hoje, vamos conectar a sua API à necessidade do Front-end: o cadastro e login de usuários.

Nesta aula, focaremos em criar os Schemas (Pydantic) que servirão de ponte entre o formulário que vocês criaram no Front e o banco de dados que usaremos em breve.

# 1. O que é CRUD?

CRUD é o acrônimo para as quatro operações básicas de qualquer sistema que manipula dados:

Create (Criar): Adicionar um novo usuário.

Read (Ler): Buscar os dados de um usuário ou listar todos.

Update (Atualizar): Alterar a senha ou a foto do perfil.

Delete (Excluir): Remover uma conta do sistema.

Relação com o Protocolo HTTP

Para cada ação do CRUD, o protocolo HTTP possui um Verbo correspondente:

Ação CRUD
Verbo HTTP
Status Code (Sucesso)
Create
POST
201 Created
Read
GET
200 OK
Update
PUT / PATCH
200 OK
Delete
DELETE
204 No Content

## 2. Definindo o Contrato (Schemas)

Os alunos do Front-end já definiram o que precisam enviar. Nosso trabalho é garantir que o Back-end entenda e valide esses dados.

No arquivo fast_zero/schemas.py, vamos estruturar três modelos:

UserSchema: O que o usuário envia (inclui a senha).

UserPublic: O que a API devolve (Segurança: NUNCA devolvemos a senha).

UserDB: Como o dado será representado internamente (com ID).

#Prática: fast_zero/schemas.py

```python
from pydantic import BaseModel, EmailStr

# O que o Front-end envia para o Cadastro
class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

# O que a API responde publicamente (Sem a senha!)
class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr

# Como o dado fica no Banco de Dados
class UserDB(UserSchema):
    id: int

```

##3. Implementando a Rota de Cadastro (POST)

Agora, vamos criar a rota no fast_zero/app.py. Por enquanto, como não conectamos o Postgres ainda, usaremos uma lista na memória do Python para simular o banco.

#Prática: fast_zero/app.py

```python
from http import HTTPStatus
from fastapi import FastAPI
from fast_zero.schemas import UserPublic, UserSchema, UserDB

app = FastAPI()

# Banco de dados temporário (em memória)
database = []

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
```

#4. Por que o Pydantic é importante?

Se o aluno do Front-end esquecer de enviar o email ou enviar um formato inválido, o Pydantic:

Barra a requisição automaticamente.

Retorna um erro 422 Unprocessable Entity.

Protege o seu banco de dados de receber "lixo".

📖 Onde testar?

Abra o seu laboratório no navegador:
https://labXX.inetz.com.br/docs (Substitua XX pelo seu número).

Clique em POST /users/.

Clique em Try it out.

Envie os dados e veja o código 201 retornar o usuário com um id, mas sem a password.

🚩 Desafio

Tente enviar um e-mail sem o "@" e veja o Pydantic trabalhando na validação!