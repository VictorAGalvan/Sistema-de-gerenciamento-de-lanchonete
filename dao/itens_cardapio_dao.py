from sqlalchemy import text

from database.conexao import engine
from models.ItensCardapio import ItensCardapio
from models.Ingrediente import Ingrediente


class ItensCardapioDAO:

    def select(self):
        with engine.connect() as connection:
            resultado = connection.execute(text("""
                SELECT id, nome, preco, categoria
                FROM itensCardapio
            """))

            itens = []
            for row in resultado:
                itens.append(
                    ItensCardapio(
                        id=row.id,
                        nome=row.nome,
                        preco=row.preco,
                        categoria=row.categoria,
                    )
                )
            return itens

    def insert(self, item: ItensCardapio):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    INSERT INTO itensCardapio
                        (nome, preco, categoria)
                    VALUES
                        (:nome, :preco, :categoria)
                """),
                {
                    "nome": item.nome,
                    "preco": item.preco,
                    "categoria": item.categoria,
                },
            )

    def update(self, item: ItensCardapio):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    UPDATE itensCardapio
                    SET nome = :nome,
                        preco = :preco,
                        categoria = :categoria
                    WHERE id = :id
                """),
                {
                    "id": item.id,
                    "nome": item.nome,
                    "preco": item.preco,
                    "categoria": item.categoria,
                },
            )

    def delete(self, item: ItensCardapio):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    DELETE FROM itensCardapio
                    WHERE id = :id
                """),
                {"id": item.id},
            )

    def selectID(self, id: int):
        with engine.connect() as connection:
            row = connection.execute(
                text("""
                    SELECT id, nome, preco, categoria
                    FROM itensCardapio
                    WHERE id = :id
                """),
                {"id": id},
            ).fetchone()

            if row is not None:
                return ItensCardapio(
                    id=row.id,
                    nome=row.nome,
                    preco=row.preco,
                    categoria=row.categoria,
                )
            return None

    def selectIngredientes(self, id_item: int):
        """Ingredientes de um item do cardápio,
        via tabela itemIngredienteCardapio."""
        with engine.connect() as connection:
            resultado = connection.execute(
                text("""
                    SELECT g.id, g.nome, g.unidade, g.quantidade
                    FROM itemIngredienteCardapio icg
                    JOIN ingredientes g
                        ON g.id = icg.idingredientes
                    WHERE icg.iditensCardapio = :id_item
                """),
                {"id_item": id_item},
            )

            return [
                Ingrediente(
                    id=row.id,
                    nome=row.nome,
                    unidade=row.unidade,
                    quantidade=row.quantidade,
                )
                for row in resultado
            ]

    def insertIngrediente(self, id_item: int, id_ingrediente: int):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    INSERT INTO itemIngredienteCardapio
                        (iditensCardapio, idingredientes)
                    VALUES
                        (:id_item, :id_ingrediente)
                """),
                {"id_item": id_item, "id_ingrediente": id_ingrediente},
            )

    def deleteIngredientes(self, id_item: int):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    DELETE FROM itemIngredienteCardapio
                    WHERE iditensCardapio = :id_item
                """),
                {"id_item": id_item},
            )
