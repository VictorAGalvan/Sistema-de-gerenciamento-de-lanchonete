from sqlalchemy import text

from database.conexao import engine
from models.Cardapio import Cardapio

class CardapioDAO:
    def select(self):
        with engine.connect() as connection:
            resultado = connection.execute(text("""
                SELECT id, data, versao
                FROM Cardapios
            """))

            cardapios = []

            for row in resultado:
                cardapio = Cardapio(
                    id=row.id,
                    data=row.data,
                    versao=row.versao,
                    itens=[]  # Inicializa a lista de itens como vazia
                )
                cardapios.append(cardapio)

            return cardapios
    def insert(self, cardapio: Cardapio):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    INSERT INTO Cardapios
                        (data, versao)
                    VALUES
                        (:data, :versao)
                """),
                {
                    "data": cardapio.data,
                    "versao": cardapio.versao,
                },
            )
    def update(self, cardapio: Cardapio):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    UPDATE Cardapios
                    SET data = :data,
                        versao = :versao
                    WHERE id = :id
                """),
                {
                    "data": cardapio.data,
                    "versao": cardapio.versao,
                    "id": cardapio.id,
                },
            )
    def delete(self, cardapio: Cardapio):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    DELETE FROM Cardapios
                    WHERE id = :id
                """),
                {"id": cardapio.id},
            )
    def selectID(self, id: int):
        with engine.connect() as connection:
            resultado = connection.execute(
                text("""
                    SELECT id, data, versao
                    FROM Cardapios
                    WHERE id = :id
                """),
                {"id": id},
            ).fetchone()

            if resultado:
                return Cardapio(
                    id=resultado.id,
                    data=resultado.data,
                    versao=resultado.versao,
                    itens=[]  # Inicializa a lista de itens como vazia
                )
            else:
                return None