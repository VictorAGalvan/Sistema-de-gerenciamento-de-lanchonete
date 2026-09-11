from sqlalchemy import text

from database.conexao import engine
from models.Cardapio import Cardapio
from models.ItensCardapio import ItensCardapio


class CardapioDAO:
    def select(self):
        with engine.connect() as connection:
            resultado = connection.execute(text("""
                SELECT c.id,
                       c.data,
                       c.versao,
                       i.id      AS item_id,
                       i.nome    AS item_nome,
                       i.preco   AS item_preco,
                       i.categoria AS item_categoria
                FROM cardapios c
                LEFT JOIN itensCardapio i
                    ON i.id = c.iditensCardapio
                ORDER BY c.data, c.versao
            """))

            cardapios = []
            indice = {}

            for row in resultado:
                chave = (row.data, row.versao)
                if chave not in indice:
                    cardapio = Cardapio(
                        id=row.id, data=row.data, versao=row.versao, itens=[]
                    )
                    cardapios.append(cardapio)
                    indice[chave] = cardapio

                if row.item_id is not None:
                    indice[chave].itens.append(
                        ItensCardapio(
                            id=row.item_id,
                            nome=row.item_nome,
                            preco=row.item_preco,
                            categoria=row.item_categoria,
                        )
                    )

            return cardapios

    def insert(self, cardapio: Cardapio):
        with engine.begin() as connection:
            if cardapio.itens:
                for item in cardapio.itens:
                    connection.execute(
                        text("""
                            INSERT INTO cardapios
                                (iditensCardapio, data, versao)
                            VALUES
                                (:id_item, :data, :versao)
                        """),
                        {
                            "id_item": item.id,
                            "data": cardapio.data,
                            "versao": cardapio.versao,
                        },
                    )
            else:
                connection.execute(
                    text("""
                        INSERT INTO cardapios
                            (iditensCardapio, data, versao)
                        VALUES
                            (NULL, :data, :versao)
                    """),
                    {
                        "data": cardapio.data,
                        "versao": cardapio.versao,
                    },
                )

    def update(self, cardapio: Cardapio):
        with engine.begin() as connection:
            row = connection.execute(
                text("""
                    SELECT data, versao
                    FROM cardapios
                    WHERE id = :id
                """),
                {"id": cardapio.id},
            ).fetchone()

            if not row:
                return

            connection.execute(
                text("""
                    DELETE FROM cardapios
                    WHERE data = :data_antiga
                      AND versao = :versao_antiga
                """),
                {
                    "data_antiga": row.data,
                    "versao_antiga": row.versao,
                },
            )

            if cardapio.itens:
                for item in cardapio.itens:
                    connection.execute(
                        text("""
                            INSERT INTO cardapios
                                (iditensCardapio, data, versao)
                            VALUES
                                (:id_item, :data, :versao)
                        """),
                        {
                            "id_item": item.id,
                            "data": cardapio.data,
                            "versao": cardapio.versao,
                        },
                    )
            else:
                connection.execute(
                    text("""
                        INSERT INTO cardapios
                            (iditensCardapio, data, versao)
                        VALUES
                            (NULL, :data, :versao)
                    """),
                    {
                        "data": cardapio.data,
                        "versao": cardapio.versao,
                    },
                )

    def delete(self, cardapio: Cardapio):
        with engine.begin() as connection:
            row = connection.execute(
                text("""
                    SELECT data, versao
                    FROM cardapios
                    WHERE id = :id
                """),
                {"id": cardapio.id},
            ).fetchone()

            if not row:
                return

            connection.execute(
                text("""
                    DELETE FROM cardapios
                    WHERE data = :data
                      AND versao = :versao
                """),
                {
                    "data": row.data,
                    "versao": row.versao,
                },
            )

    def selectID(self, id: int):
        with engine.connect() as connection:
            row = connection.execute(
                text("""
                    SELECT id, data, versao
                    FROM cardapios
                    WHERE id = :id
                """),
                {"id": id},
            ).fetchone()

            if not row:
                return None

            cardapio = Cardapio(id=row.id, data=row.data, versao=row.versao, itens=[])

            resultado = connection.execute(
                text("""
                SELECT i.id, i.nome, i.preco, i.categoria
                FROM cardapios c
                JOIN itensCardapio i
                    ON i.id = c.iditensCardapio
                WHERE c.data = :data
                  AND c.versao = :versao
            """),
                {"data": row.data, "versao": row.versao},
            )

            for item_row in resultado:
                cardapio.itens.append(
                    ItensCardapio(
                        id=item_row.id,
                        nome=item_row.nome,
                        preco=item_row.preco,
                        categoria=item_row.categoria,
                    )
                )

            return cardapio
