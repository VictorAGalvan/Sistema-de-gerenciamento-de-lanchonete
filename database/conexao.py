from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.base import Base
# from models import *
from models.Ingrediente import Ingrediente
nome = "lancheriaDB"
user = "postgres"
password = "postgres"
host = "localhost"
port = "5432"
DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{nome}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

def inicializar_banco():
    Base.metadata.create_all(engine)
