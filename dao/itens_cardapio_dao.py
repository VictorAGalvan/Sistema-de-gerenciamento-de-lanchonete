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
            return [
                ItensCardapio(
                    id=row.id, nome=row.nome, preco=row.preco,
                    categoria=row.categoria, ingredientes=self.selectIngredientes(row.id)
                )
                for row in resultado
            ]

    def selectID(self, id: int):
        with engine.connect() as connection:
            row = connection.execute(
                text("SELECT id, nome, preco, categoria FROM itensCardapio WHERE id = :id"),
                {"id": id},
            ).fetchone()
            if row is None:
                return None
            return ItensCardapio(
                id=row.id, nome=row.nome, preco=row.preco,
                categoria=row.categoria, ingredientes=self.selectIngredientes(row.id)
            )

    def insert(self, item: ItensCardapio):
        with engine.begin() as connection:
            resultado = connection.execute(
                text("""
                    INSERT INTO itensCardapio (nome, preco, categoria)
                    VALUES (:nome, :preco, :categoria)
                    RETURNING id
                """),
                {"nome": item.nome, "preco": item.preco, "categoria": item.categoria},
            )
            item.id = resultado.scalar()

    def update(self, item: ItensCardapio):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    UPDATE itensCardapio
                    SET nome = :nome, preco = :preco, categoria = :categoria
                    WHERE id = :id
                """),
                {"id": item.id, "nome": item.nome, "preco": item.preco, "categoria": item.categoria},
            )

    def delete(self, item: ItensCardapio):
        self.deleteIngredientes(item.id)
        with engine.begin() as connection:
            connection.execute(text("DELETE FROM itensCardapio WHERE id = :id"), {"id": item.id})

    def selectIngredientes(self, id_item: int):
        with engine.connect() as connection:
            resultado = connection.execute(
                text("""
                    SELECT g.id, g.nome, g.unidade, g.quantidade
                    FROM itemIngredienteCardapio icg
                    JOIN ingredientes g ON g.id = icg.idingredientes
                    WHERE icg.iditensCardapio = :id_item
                """),
                {"id_item": id_item},
            )
            return [Ingrediente(id=r.id, nome=r.nome, unidade=r.unidade, quantidade=r.quantidade) for r in resultado]

    def insertIngrediente(self, id_item: int, id_ingrediente: int):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    INSERT INTO itemIngredienteCardapio (iditensCardapio, idingredientes)
                    VALUES (:id_item, :id_ingrediente)
                """),
                {"id_item": id_item, "id_ingrediente": id_ingrediente},
            )

    def deleteIngredientes(self, id_item: int):
        with engine.begin() as connection:
            connection.execute(
                text("DELETE FROM itemIngredienteCardapio WHERE iditensCardapio = :id_item"),
                {"id_item": id_item},
            )