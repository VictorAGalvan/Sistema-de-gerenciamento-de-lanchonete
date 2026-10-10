from sqlalchemy import text

from database.conexao import engine
from models.Ingrediente import Ingrediente


class IngredienteDAO:

    def select(self):

        with engine.connect() as connection:

            resultado = connection.execute(text("""
                    SELECT id, nome, unidade, quantidade
                    FROM Ingredientes
                """))

            ingredientes = []

            for row in resultado:

                ingrediente = Ingrediente(
                    id=row.id,
                    nome=row.nome,
                    unidade=row.unidade,
                    quantidade=row.quantidade,
                )

                ingredientes.append(ingrediente)

            return ingredientes

    def insert(self, ingrediente: Ingrediente):

        with engine.begin() as connection:

            connection.execute(
                text("""
                    INSERT INTO Ingredientes
                        (nome, unidade, quantidade)
                    VALUES
                        (:nome, :unidade, :quantidade)
                """),
                {
                    "nome": ingrediente.nome,
                    "unidade": ingrediente.unidade,
                    "quantidade": ingrediente.quantidade,
                },
            )

    def update(self, ingrediente: Ingrediente):

        with engine.begin() as connection:

            connection.execute(
                text("""
                    UPDATE Ingredientes
                    SET nome = :nome,
                        unidade = :unidade,
                        quantidade = :quantidade
                    WHERE id = :id
                """),
                {
                    "id": ingrediente.id,
                    "nome": ingrediente.nome,
                    "unidade": ingrediente.unidade,
                    "quantidade": ingrediente.quantidade,
                },
            )

    def restock(self, id_ingrediente: int, quantidade: int):
        with engine.begin() as connection:
            resultado = connection.execute(
                text("""
                    UPDATE Ingredientes
                    SET quantidade = quantidade + :quantidade
                    WHERE id = :id
                    RETURNING id
                """),
                {"id": id_ingrediente, "quantidade": quantidade},
            )
            if resultado.scalar() is None:
                raise LookupError(f"Ingrediente {id_ingrediente} não encontrado.")

    def delete(self, ingrediente: Ingrediente):
        with engine.begin() as connection:

            connection.execute(
                text("""
                    DELETE FROM Ingredientes
                    WHERE id = :id
                """),
                {"id": ingrediente.id},
            )

    def selectID(self, id: int):

        with engine.connect() as connection:

            resultado = connection.execute(
                text("""
                    SELECT id, nome, unidade, quantidade
                    FROM Ingredientes
                    WHERE id = :id
                """),
                {"id": id},
            )

            row = resultado.fetchone()

            if row is not None:
                ingrediente = Ingrediente(
                    id=row.id,
                    nome=row.nome,
                    unidade=row.unidade,
                    quantidade=row.quantidade,
                )
                return ingrediente
            else:
                return None
