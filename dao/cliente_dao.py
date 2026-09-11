from sqlalchemy import text

from database.conexao import engine
from models.Cliente import Cliente

class ClienteDAO:

    def select(self):
        sql = text("""
            SELECT id, nome, cpf, telefone
            FROM clientes
        """)
        with engine.connect() as connection:
            resultado = connection.execute(sql)
            clientes = []
            for row in resultado:
                clientes.append(
                    Cliente(
                        id=row.id,
                        nome=row.nome,
                        cpf=row.cpf,
                        telefone=row.telefone,
                    )
                )
            return clientes

    def insert(self, cliente):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    INSERT INTO clientes (nome, cpf, telefone)
                    VALUES (:nome, :cpf, :telefone)
                """),
                {
                    "nome": cliente.nome,
                    "cpf": cliente.cpf,
                    "telefone": cliente.telefone,
                },
            )

    def update(self, cliente):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    UPDATE clientes
                    SET nome = :nome,
                        cpf = :cpf,
                        telefone = :telefone
                    WHERE id = :id
                """),
                {
                    "nome": cliente.nome,
                    "cpf": cliente.cpf,
                    "telefone": cliente.telefone,
                    "id": cliente.id,
                },
            )

    def delete(self, id_cliente):
        with engine.begin() as connection:
            connection.execute(
                text("DELETE FROM clientes WHERE id = :id"),
                {"id": id_cliente},
            )

    def selectID(self, id_cliente):
        sql = text("""
            SELECT id, nome, cpf, telefone
            FROM clientes
            WHERE id = :id
        """)
        with engine.connect() as connection:
            resultado = connection.execute(sql, {"id": id_cliente})
            row = resultado.fetchone()
            if row:
                return Cliente(
                    id=row.id,
                    nome=row.nome,
                    cpf=row.cpf,
                    telefone=row.telefone,
                )
            else:
                return None
