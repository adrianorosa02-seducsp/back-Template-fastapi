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