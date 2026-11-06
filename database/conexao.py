from datetime import date

from sqlalchemy import create_engine, text as sql_text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from database.base import Base
import models.Ingrediente   # registra entidades no Base.metadata
import models.Cliente
import models.Cardapio
import models.ItensCardapio

nome = "lanchoneteDB"
user = "postgres"
password = "admin"
host = "localhost"
port = "5432"
DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{nome}"

ADMIN_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/postgres"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)


def criar_banco():
    try:
        with engine.connect():
            return  # banco existe e aceita conexão
    except OperationalError:
        pass

    admin_engine = create_engine(ADMIN_URL, isolation_level="AUTOCOMMIT")
    with admin_engine.connect() as connection:
        existe = connection.execute(
            sql_text("SELECT 1 FROM pg_database WHERE datname = :nome"),
            {"nome": nome},
        ).fetchone()
        if not existe:
            connection.execute(sql_text(f'CREATE DATABASE "{nome}"'))
    admin_engine.dispose()


def inicializar_banco():
    criar_banco()
    import dao.itens_pedido_dao  
    import dao.pedido_dao        
    Base.metadata.create_all(engine)
    defaultCardapio()


def defaultCardapio():
    from models.Cardapio import Cardapio

    with SessionLocal() as session:
        existe = session.query(Cardapio).first()
        if not existe:
            session.add(Cardapio(data=date.today(), versao="1.0", ativo=True))
            session.commit()
