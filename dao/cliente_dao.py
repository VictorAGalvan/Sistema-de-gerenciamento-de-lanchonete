from sqlalchemy import text

from database.conexao import engine
from models.Cliente import Cliente

class ClienteDAO:

    def select(self):
        sql = text("""
            SELECT id, nome, cpf, telefone, senha
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
                        senha=row.senha,
                    )
                )
            return clientes

    def insert(self, cliente):
        with engine.begin() as connection:
            resultado = connection.execute(
                text("""
                    INSERT INTO clientes (nome, cpf, telefone, senha)
                    VALUES (:nome, :cpf, :telefone, :senha)
                    RETURNING id
                """),
                {
                    "nome": cliente.nome,
                    "cpf": cliente.cpf,
                    "telefone": cliente.telefone,
                    "senha": cliente.senha,
                },
            )
            cliente.id = resultado.scalar()

    def update(self, cliente):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    UPDATE clientes
                    SET nome = :nome,
                        cpf = :cpf,
                        telefone = :telefone,
                        senha = :senha
                    WHERE id = :id
                """),
                {
                    "nome": cliente.nome,
                    "cpf": cliente.cpf,
                    "telefone": cliente.telefone,
                    "senha": cliente.senha,
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
            SELECT id, nome, cpf, telefone, senha
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
                    senha=row.senha,
                )
            else:
                return None

    def selectNome(self, nome):
        sql = text("""
            SELECT id, nome, cpf, telefone, senha
            FROM clientes
            WHERE nome = :nome
        """)
        with engine.connect() as connection:
            resultado = connection.execute(sql, {"nome": nome})
            row = resultado.fetchone()
            if row:
                return Cliente(
                    id=row.id,
                    nome=row.nome,
                    cpf=row.cpf,
                    telefone=row.telefone,
                    senha=row.senha,
                )
            else:
                return None