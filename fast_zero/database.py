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
