from sqlalchemy import text

from database.conexao import engine
from models.ItensPedido import ItensPedidos
from models.ItensCardapio import ItensCardapio


class ItensPedidoDAO:

    def select(self):
        with engine.connect() as connection:
            resultado = connection.execute(text("""
                SELECT ip.id,
                       ip.quantidade,
                       ip.observacao,
                       i.id        AS item_id,
                       i.nome      AS item_nome,
                       i.preco     AS item_preco,
                       i.categoria AS item_categoria
                FROM itensPedido ip
                JOIN itensCardapio i
                    ON i.id = ip.iditensCardapio
                ORDER BY ip.id
            """))

            itens = []
            for row in resultado:
                item_cardapio = ItensCardapio(
                    id=row.item_id,
                    nome=row.item_nome,
                    preco=row.item_preco,
                    categoria=row.item_categoria,
                )
                itens.append(
                    ItensPedidos(
                        pedido=None,
                        item_cardapio=item_cardapio,
                        quantidade=row.quantidade,
                        observacao=row.observacao,
                        nome=row.item_nome,
                        preco=row.item_preco,
                        categoria=row.item_categoria,
                    )
                )
            return itens

    def insert(self, item: ItensPedidos):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    INSERT INTO itensPedido
                        (iditensCardapio, quantidade, observacao)
                    VALUES
                        (:id_item, :quantidade, :observacao)
                """),
                {
                    "id_item": item.item_cardapio.id,
                    "quantidade": item.quantidade,
                    "observacao": item.observacao,
                },
            )

    def update(self, id_item, item: ItensPedidos):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    UPDATE itensPedido
                    SET iditensCardapio = :id_item_cardapio,
                        quantidade = :quantidade,
                        observacao = :observacao
                    WHERE id = :id
                """),
                {
                    "id": id_item,
                    "id_item_cardapio": item.item_cardapio.id,
                    "quantidade": item.quantidade,
                    "observacao": item.observacao,
                },
            )

    def delete(self, id_item):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    DELETE FROM itensPedido
                    WHERE id = :id
                """),
                {"id": id_item},
            )

    def selectID(self, id_item):
        with engine.connect() as connection:
            row = connection.execute(
                text("""
                    SELECT ip.id,
                           ip.quantidade,
                           ip.observacao,
                           i.id        AS item_id,
                           i.nome      AS item_nome,
                           i.preco     AS item_preco,
                           i.categoria AS item_categoria
                    FROM itensPedido ip
                    JOIN itensCardapio i
                        ON i.id = ip.iditensCardapio
                    WHERE ip.id = :id
                """),
                {"id": id_item},
            ).fetchone()

            if row is None:
                return None

            item_cardapio = ItensCardapio(
                id=row.item_id,
                nome=row.item_nome,
                preco=row.item_preco,
                categoria=row.item_categoria,
            )
            return ItensPedidos(
                pedido=None,
                item_cardapio=item_cardapio,
                quantidade=row.quantidade,
                observacao=row.observacao,
                nome=row.item_nome,
                preco=row.item_preco,
                categoria=row.item_categoria,
            )
