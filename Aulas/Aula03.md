📘 Aula-03: Conectando ao Banco de Dados (PostgreSQL)

Até agora, nossos usuários sumiam sempre que o servidor reiniciava. Hoje, vamos conectar nossa API ao PostgreSQL do laboratório para que os dados sejam salvos permanentemente.

1. O motor da conexão: SQLAlchemy

Para não precisarmos escrever SQL puro (como INSERT INTO...), usamos um ORM (Object-Relational Mapper) chamado SQLAlchemy. Ele transforma nossas classes Python em tabelas no banco de dados.

Configurações do Ambiente Inetz:

Host: db.inetz.com.br
Porta: 5432
Banco: appdb
Usuário: appuser
Senha: appsenha

2. Configurando o Banco de Dados

Vamos criar um novo arquivo chamado fast_zero/database.py para centralizar a conexão.

Prática: fast_zero/database.py
```python
from sqlalchemy import create_url, create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.schema import MetaData

# URL de conexão (Padrão: postgresql://user:password@host:port/db)
DATABASE_URL = "postgresql://appuser:appsenha@db.inetz.com.br:5432/appdb"

# O Motor da conexão
engine = create_engine(DATABASE_URL)

# Classe Base para nossos modelos
class Base(DeclarativeBase):
    pass

# Função para pegar uma sessão do banco
def get_session():
    with Session(engine) as session:
        yield session

```
## 3. Criando a Tabela de Usuários

Agora, vamos dizer ao SQLAlchemy como a tabela users deve ser no Postgres. Criaremos o arquivo fast_zero/models.py.

Prática: fast_zero/models.py

from sqlalchemy.orm import Mapped, mapped_column
from fast_zero.database import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)


4. Integrando no app.py (O grande momento!)

Agora vamos mudar a nossa rota POST /users/ para salvar no banco real em vez daquela lista database = [].

Prática: fast_zero/app.py

from http import HTTPStatus
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from fast_zero.database import get_session, engine, Base
from fast_zero.models import User
from fast_zero.schemas import UserPublic, UserSchema

app = FastAPI()

# Cria as tabelas no banco de dados (se não existirem)
Base.metadata.create_all(bind=engine)

@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    # 1. Verificar se o usuário já existe no banco
    db_user = session.scalar(select(User).where(User.email == user.email))
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # 2. Criar o objeto do banco
    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password  # Na próxima aula aprenderemos a Hashear!
    )

    # 3. Salvar e confirmar (Commit)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


📖 Como verificar?

Execute sua API.

Faça um cadastro no Swagger.

Reinicie o servidor.

Se o cadastro continuar lá (verificaremos com o GET na próxima aula), seu banco de dados está configurado com sucesso!

🚩 Desafio

O que acontece se você tentar cadastrar o mesmo e-mail duas vezes agora que temos a validação if db_user? Teste e observe o erro 400.