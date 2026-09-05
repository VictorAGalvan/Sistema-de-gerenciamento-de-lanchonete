from sqlalchemy import text

from database.conexao import engine
from models.Cliente import Cliente

class ClienteDAO:
    
    def select(self):
        sql = text("SELECT * FROM clientes")
        with engine.connect() as connection:
            resultado = connection.execute(sql)
            clientes = []
            for row in resultado:
                clientes.append(Cliente(id=row.id, nome=row.nome))
            return clientes

    def insert(self, cliente):
        with engine.begin() as connection:
            connection.execute(
                text("INSERT INTO clientes (nome) VALUES (:nome)"),
                {"nome": cliente.nome},
            )

    def update(self, cliente):
        with engine.begin() as connection:
            connection.execute(
                text("UPDATE clientes SET nome = :nome WHERE id = :id"),
                {"nome": cliente.nome, "id": cliente.id},
            )

    def delete(self, id_cliente):
        with engine.begin() as connection:
            connection.execute(
                text("DELETE FROM clientes WHERE id = :id"),
                {"id": id_cliente},
            )

    def selectID(self, id_cliente):
        sql = text("SELECT * FROM clientes WHERE id = :id")
        with engine.connect() as connection:
            resultado = connection.execute(sql, {"id": id_cliente})
            row = resultado.fetchone()
            if row:
                return Cliente(id=row.id, nome=row.nome)
            else:
                return None
