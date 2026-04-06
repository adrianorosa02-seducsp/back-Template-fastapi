# 📘 Aula-03: Persistência Real com PostgreSQL e SQLAlchemy

Com os endpoints da nossa API já estabelecidos, estamos, por ora, utilizando um banco de dados simulado, armazenando uma lista em memória. Nesta aula, iniciaremos o processo de configuração do nosso banco de dados real.

Nossa agenda inclui a instalação do SQLAlchemy, a definição do modelo de usuários e a integração com o banco de dados evolutivo. Além disso, exploraremos como desacoplar as configurações do banco de dados da aplicação, seguindo os princípios dos 12 fatores.

## 1. O que é um ORM e por que usamos um?

ORM significa Mapeamento Objeto-Relacional. É uma técnica de programação que vincula (ou mapeia) objetos a registros de banco de dados. Em outras palavras, um ORM permite que você interaja com seu banco de dados como se estivesse trabalhando com objetos Python.

O SQLAlchemy é um exemplo de ORM. Ele permite que você trabalhe com bancos de dados SQL de maneira mais natural aos programadores Python.

## Por que usar um ORM?

Abstração de banco de dados: Mude de banco com poucas alterações no código.
Segurança: Lida nativamente com a prevenção de Injeções SQL.
Eficiência: Gera esquemas e realiza migrações automaticamente.

## 2. Configurações de ambiente e os 12 fatores

Uma boa prática é separar as configurações do código, especialmente dados sensíveis. Isso está alinhada com a metodologia dos 12 fatores (fator 3: Config).

Para gerenciar isso de forma segura, usaremos o pydantic-settings.

# 🛠️ Passo 01: Instalação de Dependências

Abra o terminal no seu VS Code e execute:

## Adiciona suporte a configurações por ambiente
poetry add pydantic-settings

## Adiciona o ORM SQLAlchemy
poetry add sqlalchemy

## Adiciona o driver para conectar ao PostgreSQL
poetry add psycopg2-binary


# 3. O básico sobre SQLAlchemy: Engine e Session

Engine: É o ponto de contato com o banco de dados. Ela gerencia as conexões físicas.

Session: É a interface principal para transações (salvar, buscar, deletar).

# 4. Definindo os Modelos de Dados (Models)

Os modelos definem a estrutura de como os dados serão armazenados. Usaremos o mapped_as_dataclass para que nossas classes se comportem como dataclasses modernas.

## Prática: Criar fast_zero/models.py
```python
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column, registry

table_registry = registry()

@mapped_as_dataclass(table_registry)
class User:
    __tablename__ = 'users'

    # id e created_at são gerados pelo banco (init=False)
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
```

# 5. Configurando a Conexão (Database)

Agora, vamos configurar a conexão com o banco de dados do ambiente Labs-Seduc.

Credenciais:

Host: db.inetz.com.br
Banco: appdb
User: appuser / Senha: appsenha

## Prática: Criar fast_zero/database.py
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fast_zero.models import table_registry

# URI de Conexão padrão PostgreSQL
DATABASE_URL = "postgresql://appuser:appsenha@db.inetz.com.br:5432/appdb"

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

def create_db():
    # Cria as tabelas fisicamente no Postgres
    table_registry.metadata.create_all(bind=engine)

```

# 6. Integrando no app.py

Vamos substituir a lista em memória pela persistência real.
```python
from http import HTTPStatus
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from fast_zero.database import get_session, create_db
from fast_zero.models import User
from fast_zero.schemas import UserPublic, UserSchema

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
```

🚩 Desafio da Aula

Tente cadastrar um usuário no Swagger e verifique no console se houve algum erro de conexão. Se o retorno for 201, parabéns! Seu usuário agora sobrevive ao reinício do servidor.