from sqlalchemy import text

from database.conexao import engine
from models.ItensPedido import ItensPedido
from models.ItensCardapio import ItensCardapio
from models.Ingrediente import Ingrediente


class ItensPedidoDAO:

    def select(self):
        with engine.connect() as connection:
            resultado = connection.execute(text("""
                SELECT ip.id, ip.quantidade, ip.observacao,
                       i.id AS item_id, i.nome AS item_nome, i.preco AS item_preco, i.categoria AS item_categoria
                FROM itensPedido ip
                JOIN itensCardapio i ON i.id = ip.iditensCardapio
                ORDER BY ip.id
            """))
            itens = []
            for row in resultado:
                item_cardapio = ItensCardapio(id=row.item_id, nome=row.item_nome, preco=row.item_preco, categoria=row.item_categoria, ingredientes=[])
                item_pedido = ItensPedido(item_cardapio, quantidade=row.quantidade, observacao=row.observacao or "")
                item_pedido.id = row.id  # sobrescreve o id herdado do item_cardapio pelo id real da linha
                item_pedido.ingredientes = self.selectIngredientes(row.id)
                itens.append(item_pedido)
            return itens

    def selectID(self, id_item):
        with engine.connect() as connection:
            row = connection.execute(
                text("""
                    SELECT ip.id, ip.quantidade, ip.observacao,
                           i.id AS item_id, i.nome AS item_nome, i.preco AS item_preco, i.categoria AS item_categoria
                    FROM itensPedido ip
                    JOIN itensCardapio i ON i.id = ip.iditensCardapio
                    WHERE ip.id = :id
                """),
                {"id": id_item},
            ).fetchone()
            if row is None:
                return None
            item_cardapio = ItensCardapio(id=row.item_id, nome=row.item_nome, preco=row.item_preco, categoria=row.item_categoria, ingredientes=[])
            item_pedido = ItensPedido(item_cardapio, quantidade=row.quantidade, observacao=row.observacao or "")
            item_pedido.id = row.id
            item_pedido.ingredientes = self.selectIngredientes(row.id)
            return item_pedido

    def insert(self, item: ItensPedido):
        with engine.begin() as connection:
            resultado = connection.execute(
                text("""
                    INSERT INTO itensPedido (iditensCardapio, quantidade, observacao)
                    VALUES (:id_item_cardapio, :quantidade, :observacao)
                    RETURNING id
                """),
                {"id_item_cardapio": item.id, "quantidade": item.quantidade, "observacao": item.observacao},
            )
            item.id = resultado.scalar()

    def update(self, item: ItensPedido):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    UPDATE itensPedido
                    SET quantidade = :quantidade, observacao = :observacao
                    WHERE id = :id
                """),
                {"id": item.id, "quantidade": item.quantidade, "observacao": item.observacao},
            )

    def delete(self, item: ItensPedido):
        self.deleteIngredientes(item.id)
        with engine.begin() as connection:
            connection.execute(text("DELETE FROM itensPedido WHERE id = :id"), {"id": item.id})

    def selectIngredientes(self, id_item_pedido: int):
        with engine.connect() as connection:
            resultado = connection.execute(
                text("""
                    SELECT g.id, g.nome, g.unidade, g.quantidade
                    FROM itemIngredienteItensPedido iip
                    JOIN ingredientes g ON g.id = iip.idingredientes
                    WHERE iip.iditensPedido = :id_item_pedido
                """),
                {"id_item_pedido": id_item_pedido},
            )
            return [Ingrediente(id=r.id, nome=r.nome, unidade=r.unidade, quantidade=r.quantidade) for r in resultado]

    def insertIngrediente(self, id_item_pedido: int, id_ingrediente: int):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    INSERT INTO itemIngredienteItensPedido (iditensPedido, idingredientes)
                    VALUES (:id_item_pedido, :id_ingrediente)
                """),
                {"id_item_pedido": id_item_pedido, "id_ingrediente": id_ingrediente},
            )

    def deleteIngredientes(self, id_item_pedido: int):
        with engine.begin() as connection:
            connection.execute(
                text("DELETE FROM itemIngredienteItensPedido WHERE iditensPedido = :id_item_pedido"),
                {"id_item_pedido": id_item_pedido},
            )
    def select_por_pedido(self, id_pedido: int):
        with engine.connect() as connection:
            resultado = connection.execute(
                text("""
                    SELECT ip.id, ip.quantidade, ip.observacao,
                        i.id AS item_id, i.nome AS item_nome, i.preco AS item_preco, i.categoria AS item_categoria
                    FROM itensPedido ip
                    JOIN itensCardapio i ON i.id = ip.iditensCardapio
                    WHERE ip.idpedido = :id_pedido
                """),
                {"id_pedido": id_pedido},
            )
            itens = []
            for row in resultado:
                item_cardapio = ItensCardapio(id=row.item_id, nome=row.item_nome, preco=row.item_preco, categoria=row.item_categoria, ingredientes=[])
                item_pedido = ItensPedido(item_cardapio, quantidade=row.quantidade, observacao=row.observacao or "")
                item_pedido.id = row.id
                item_pedido.ingredientes = self.selectIngredientes(row.id)
                itens.append(item_pedido)
            return itens