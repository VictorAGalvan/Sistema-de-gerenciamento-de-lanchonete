from sqlalchemy import create_engine

password = "postgres"  # senha do banco de dados
user = "postgres"   # usuário do banco de dados
port = "5432" # porta do banco de dados
database = "lanchoneteDB" # nome do banco de dados

DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@localhost:{port}/{database}"

engine = create_engine(DATABASE_URL)
